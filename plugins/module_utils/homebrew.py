# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import re

HOMEBREW_PATH_DEFAULT = "/usr/local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin"

# Errors Homebrew raises for a formula or cask name it does not know, including a cask name it
# rejects as invalid. A formula file that Homebrew finds but cannot load reports the same first
# line, followed by "In formula file:".
HOMEBREW_UNAVAILABLE = re.compile(
    r"^Error: (?:No available formula(?: or cask)? with the name \"[^\n]*$(?!\nIn formula file:)"
    r"|Cask '.*' is unavailable(?:\.$|: (?:No Cask with this name exists|Invalid cask name)\.|: '.+' does not exist\.$))",
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
    # HOMEBREW_COLOR colors "Error:" even off a TTY, and GITHUB_ACTIONS turns it into a "::error::"
    # annotation; either hides HOMEBREW_UNAVAILABLE. Homebrew ignores an empty GITHUB_ACTIONS.
    environ_update = {"HOMEBREW_NO_COLOR": "1", "GITHUB_ACTIONS": ""}
    # Ansible would otherwise expand "$VAR" and "~" in arguments into the name of another formula or cask.
    rc, stdout, stderr = module.run_command(
        [homebrew_bin(module)] + args, environ_update=environ_update, expand_user_and_vars=False
    )
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

    # "--" keeps names that begin with "-" from being parsed as brew options.
    output = homebrew_output(module, args + ["--"] + names, operation, skip_unavailable=True)
    if output is not None:
        return [output]

    outputs = [homebrew_output(module, args + ["--", name], operation, skip_unavailable=True) for name in names]

    return [output for output in outputs if output is not None]


def homebrew_unique(items, key):
    # brew repeats an item for a repeated name or for aliases of one name.
    seen = set()
    unique = []

    for item in items:
        identifier = item[key]
        if identifier in seen:
            continue

        seen.add(identifier)
        unique.append(item)

    return unique


def homebrew_info(module, kind):
    key = "casks" if kind == "cask" else "formulae"
    operation = homebrew_operation(module, kind, f"installed {key}")
    items = []

    for stdout in homebrew_outputs(module, ["info", "--json=v2", f"--{kind}"], "--installed", operation):
        items += json.loads(stdout)[key]

    return homebrew_unique(items, "full_token" if kind == "cask" else "full_name")


def homebrew_services_info(module):
    operation = homebrew_operation(module, "service", "all services")
    services = []

    for stdout in homebrew_outputs(module, ["services", "info", "--json"], "--all", operation):
        # brew prints nothing for --all when no installed formula has a service.
        if not stdout:
            continue

        services += json.loads(stdout)

    return homebrew_unique(services, "name")
