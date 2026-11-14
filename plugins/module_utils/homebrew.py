# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import re

HOMEBREW_PATH_DEFAULT = "/usr/local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin"

# Errors Homebrew raises for a formula or cask name it does not know.
HOMEBREW_UNAVAILABLE = re.compile(
    r"^Error: (?:No available formula(?: or cask)? with the name \""
    r"|Cask '[^']+' is unavailable(?:\.$|: No Cask with this name exists\.))",
    re.MULTILINE,
)


def homebrew_argument_spec():
    return {
        "name": {"elements": "str", "type": "list"},
        "path": {"default": HOMEBREW_PATH_DEFAULT, "type": "path"},
    }


def homebrew_bin(module):
    brew_bin = module.get_bin_path("brew", opt_dirs=module.params["path"].split(":"))

    if not brew_bin:
        module.fail_json(msg="Unable to locate brew executable.")

    return brew_bin


def homebrew_operation(module, kind, default):
    return f"gather Homebrew {kind} information for {', '.join(module.params['name'] or [default])}"


def homebrew_output(module, args, operation, skip_unavailable=False):
    rc, stdout, stderr = module.run_command([homebrew_bin(module)] + args)
    if rc == 0:
        return stdout

    if skip_unavailable and HOMEBREW_UNAVAILABLE.search(stderr):
        return None

    detail = stderr.strip() or stdout.strip()
    module.fail_json(msg=f"Unable to {operation}: {detail}")


def homebrew_outputs(module, args, default_arg, operation):
    names = module.params["name"]
    if not names:
        return [homebrew_output(module, args + [default_arg], operation)]

    output = homebrew_output(module, args + names, operation, skip_unavailable=True)
    if output is not None:
        return [output]

    outputs = [homebrew_output(module, args + [name], operation, skip_unavailable=True) for name in names]

    return [output for output in outputs if output is not None]


def homebrew_json(module, stdout, operation):
    try:
        return json.loads(stdout)
    except ValueError as error:
        module.fail_json(msg=f"Unable to parse brew output while {operation}: {error}")


def homebrew_items(module, items, operation):
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        module.fail_json(msg=f"Unexpected brew output while {operation}.")

    return items


def homebrew_info(module, kind):
    key = "casks" if kind == "cask" else "formulae"
    operation = homebrew_operation(module, kind, f"installed {key}")
    items = []

    for stdout in homebrew_outputs(module, ["info", "--json=v2", f"--{kind}"], "--installed", operation):
        data = homebrew_json(module, stdout, operation)
        if not isinstance(data, dict):
            module.fail_json(msg=f"Unexpected brew output while {operation}.")

        items += homebrew_items(module, data.get(key), operation)

    return items


def homebrew_services_info(module):
    operation = homebrew_operation(module, "service", "all services")
    services = []

    for stdout in homebrew_outputs(module, ["services", "info", "--json"], "--all", operation):
        # brew prints nothing for --all when no installed formula has a service.
        if not module.params["name"] and not stdout.strip():
            continue

        services += homebrew_items(module, homebrew_json(module, stdout, operation), operation)

    return services
