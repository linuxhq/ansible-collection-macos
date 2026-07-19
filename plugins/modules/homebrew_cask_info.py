#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: homebrew_cask_info
short_description: Gather information about Homebrew casks
description:
  - Gather cask information from Homebrew.
  - With O(name), gather information about the given casks, whether installed
    or not.
  - Without O(name), gather information about every installed cask.
  - Use M(linuxhq.macos.homebrew_info) to gather formula information.
author:
  - Taylor Kimball (@tkimball83)
options:
  name:
    description:
      - Cask names to gather information about.
      - When omitted, information about all installed casks is gathered.
    elements: str
    type: list
  path:
    description:
      - A V(:) separated list of paths to search for C(brew) executable.
    default: /usr/local/bin:/opt/homebrew/bin:/home/linuxbrew/.linuxbrew/bin
    type: path
requirements:
  - homebrew
"""

EXAMPLES = r"""
- name: Gather information about all installed Homebrew casks
  linuxhq.macos.homebrew_cask_info:

- name: Gather information about selected Homebrew casks
  linuxhq.macos.homebrew_cask_info:
    name:
      - iterm2
      - rectangle
"""

RETURN = r"""
---
casks:
  description: Homebrew casks.
  returned: always
  type: list
  elements: dict
  contains:
    deprecated:
      description: Whether the cask is deprecated.
      returned: always
      type: bool
    description:
      description: Short description of the cask.
      returned: always
      type: str
    installed:
      description: Installed version of the cask, or V(null) when the cask
        is not installed.
      returned: always
      type: str
    name:
      description: Cask token.
      returned: always
      type: str
    outdated:
      description: Whether the installed cask is outdated.
      returned: always
      type: bool
    tap:
      description: Tap the cask comes from.
      returned: always
      type: str
    version:
      description: Latest available version of the cask.
      returned: always
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.homebrew import (
    homebrew_argument_spec,
    homebrew_info,
)


def info(module):
    data = homebrew_info(module, "cask")

    return [
        {
            "deprecated": cask.get("deprecated", False),
            "description": cask.get("desc"),
            "installed": cask.get("installed"),
            "name": cask.get("token"),
            "outdated": cask.get("outdated", False),
            "tap": cask.get("tap"),
            "version": cask.get("version"),
        }
        for cask in data.get("casks", [])
    ]


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, casks=info(module))


if __name__ == "__main__":
    main()
