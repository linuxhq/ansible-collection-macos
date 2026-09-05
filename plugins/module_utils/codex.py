# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import os

from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict

CODEX_PATH_DEFAULT = "/usr/local/bin:/opt/homebrew/bin"


def codex_argument_spec():
    return {
        "config_dir": {"type": "path"},
        "executable": {"type": "path"},
    }


def codex_bin(module, required=True):
    executable = module.params["executable"]

    if executable:
        executable = os.path.expanduser(executable)
        if not os.path.exists(executable) and not required:
            return None
        if not os.path.isfile(executable) or not os.access(executable, os.X_OK):
            module.fail_json(msg=f"Unable to locate codex executable: {executable}")
        return executable

    executable = module.get_bin_path(
        "codex",
        opt_dirs=CODEX_PATH_DEFAULT.split(":"),
    )
    if not executable and required:
        module.fail_json(msg="Unable to locate codex executable.")

    return executable


def codex_run_json(module, args, operation):
    environment = None
    if module.params["config_dir"]:
        environment = {
            "CODEX_HOME": os.path.expanduser(module.params["config_dir"]),
        }

    command = [codex_bin(module)] + args
    rc, stdout, stderr = module.run_command(command, environ_update=environment)
    if rc != 0:
        detail = stderr.strip() or stdout.strip()
        module.fail_json(msg=f"Unable to {operation}: {detail}")

    try:
        data = json.loads(stdout)
    except ValueError as error:
        module.fail_json(msg=f"Unable to parse codex output while {operation}: {error}")

    if not isinstance(data, dict):
        module.fail_json(msg=f"Unexpected codex output while {operation}.")

    return data


def codex_list(module, args, key, operation):
    data = codex_run_json(module, args, operation)
    items = data.get(key)

    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        module.fail_json(msg=f"Unexpected codex output while {operation}.")

    return items


def codex_result(item):
    if item is None:
        return None

    return camel_dict_to_snake_dict(item)
