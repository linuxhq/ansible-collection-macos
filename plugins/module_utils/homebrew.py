# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

HOMEBREW_PATH_DEFAULT = (
    "/usr/local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin"
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


def homebrew_run_json(module, args):
    cmd = [homebrew_bin(module)] + args

    rc, stdout, stderr = module.run_command(cmd)
    if rc != 0:
        module.fail_json(
            msg="Unable to gather Homebrew information: %s" % stderr.strip()
        )

    try:
        return json.loads(stdout)
    except ValueError as e:
        module.fail_json(msg="Unable to parse brew output: %s" % e)


def homebrew_info(module, kind):
    args = ["info", "--json=v2", "--%s" % kind]

    if module.params["name"]:
        args += module.params["name"]
    else:
        args.append("--installed")

    return homebrew_run_json(module, args)


def homebrew_services_info(module):
    args = ["services", "info", "--json"]

    if module.params["name"]:
        args += module.params["name"]
    else:
        args.append("--all")

    return homebrew_run_json(module, args)
