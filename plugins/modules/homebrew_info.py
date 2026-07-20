#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: homebrew_info
short_description: Gather information about Homebrew formulae
description:
  - Gather formula information from Homebrew.
  - With O(name), gather information about the given formulae, whether
    installed or not.
  - Without O(name), gather information about every installed formula.
  - Use M(linuxhq.macos.homebrew_cask_info) to gather cask information.
author:
  - Taylor Kimball (@tkimball83)
options:
  name:
    description:
      - Formula names to gather information about.
      - When omitted, information about all installed formulae is gathered.
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
- name: Gather information about all installed Homebrew formulae
  linuxhq.macos.homebrew_info:

- name: Gather information about selected Homebrew formulae
  linuxhq.macos.homebrew_info:
    name:
      - privoxy
      - rclone
"""

RETURN = r"""
---
formulae:
  description: Homebrew formulae.
  returned: always
  type: list
  elements: dict
  contains:
    deprecated:
      description: Whether the formula is deprecated.
      returned: always
      type: bool
    description:
      description: Short description of the formula.
      returned: always
      type: str
    installed:
      description: Installed versions of the formula; empty when the formula
        is not installed.
      returned: always
      type: list
      elements: str
    name:
      description: Formula name.
      returned: always
      type: str
    outdated:
      description: Whether the installed formula is outdated.
      returned: always
      type: bool
    pinned:
      description: Whether the formula is pinned.
      returned: always
      type: bool
    tap:
      description: Tap the formula comes from.
      returned: always
      type: str
    version:
      description: Latest stable version of the formula.
      returned: always
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.homebrew import (
    homebrew_argument_spec,
    homebrew_info,
)


def info(module):
    data = homebrew_info(module, "formula")

    return [
        {
            "deprecated": formula.get("deprecated", False),
            "description": formula.get("desc"),
            "installed": [item.get("version") for item in formula.get("installed", [])],
            "name": formula.get("name"),
            "outdated": formula.get("outdated", False),
            "pinned": formula.get("pinned", False),
            "tap": formula.get("tap"),
            "version": formula.get("versions", {}).get("stable"),
        }
        for formula in data.get("formulae", [])
    ]


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, formulae=info(module))


if __name__ == "__main__":
    main()
