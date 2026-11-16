# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import os
import re

from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict

CODEX_PATH_DEFAULT = "/usr/local/bin:/opt/homebrew/bin"
CODEX_VERSION_MINIMUM = "0.153.0"


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


def codex_home(module):
    config_dir = module.params["config_dir"]
    if config_dir:
        return os.path.expanduser(config_dir)

    return os.environ.get("CODEX_HOME") or os.path.expanduser("~/.codex")


def codex_unavailable(module):
    if codex_bin(module, required=False) is None:
        return "Codex is not installed"

    home = codex_home(module)
    if not os.path.exists(home):
        return f"Codex home directory {home} does not exist"

    return None


def codex_run(module, args):
    environment = None
    if module.params["config_dir"]:
        environment = {
            "CODEX_HOME": os.path.expanduser(module.params["config_dir"]),
        }

    return module.run_command([codex_bin(module)] + args, environ_update=environment)


def codex_version_check(module):
    rc, stdout, stderr = codex_run(module, ["--version"])
    if rc != 0:
        detail = stderr.strip() or stdout.strip()
        module.fail_json(msg=f"Unable to determine Codex version: {detail}")

    output = stdout.strip()
    match = re.fullmatch(r"codex-cli ((\d+)\.(\d+)\.(\d+)(-\S+)?)", output)
    if match is None:
        module.fail_json(msg=f"Unable to parse Codex version from codex --version output: {output}")

    found = tuple(int(part) for part in match.group(2, 3, 4))
    minimum = tuple(int(part) for part in CODEX_VERSION_MINIMUM.split("."))
    # A pre-release precedes its release.
    if found < minimum or (found == minimum and match.group(5)):
        module.fail_json(msg=f"Codex {match.group(1)} is installed, but codex >= {CODEX_VERSION_MINIMUM} is required.")


def codex_run_json(module, args, operation, missing=None):
    rc, stdout, stderr = codex_run(module, args)
    if rc != 0:
        if missing is not None and missing in stderr:
            return None

        detail = stderr.strip() or stdout.strip()
        module.fail_json(msg=f"Unable to {operation}: {detail}")

    return json.loads(stdout)


def codex_list(module, args, key, operation, missing=None):
    data = codex_run_json(module, args, operation, missing)
    return None if data is None else data[key]


def codex_result(item):
    if item is None:
        return None

    return camel_dict_to_snake_dict(item)
