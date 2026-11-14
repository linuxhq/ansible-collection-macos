#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: homebrew_info
version_added: '1.1.0'
short_description: Gather information about Homebrew formulae
description:
  - Gather formula information from Homebrew.
  - With O(name), gather information about the given formulae, whether
    installed or not.
  - Names that Homebrew does not know are omitted from the results.
  - Without O(name), gather information about every installed formula.
  - Formula information is returned as reported by C(brew info --json=v2).
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
attributes:
  check_mode:
    description: This module only retrieves information and does not modify state.
    support: full
  diff_mode:
    description: Diff mode is not supported.
    support: none
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
  description:
    - Homebrew formulae as reported by C(brew info --json=v2).
    - Each item is returned unmodified; commonly used keys are listed below.
  returned: always
  type: list
  elements: dict
  contains:
    deprecated:
      description: Whether the formula is deprecated.
      returned: always
      type: bool
    desc:
      description: Short description of the formula.
      returned: always
      type: str
    full_name:
      description: Formula name qualified with its tap when the tap is not
        C(homebrew/core).
      returned: always
      type: str
    installed:
      description: Installed kegs of the formula; empty when the formula is
        not installed.
      returned: always
      type: list
      elements: dict
      contains:
        installed_on_request:
          description: Whether the keg was installed on request rather than as
            a dependency.
          returned: always
          type: bool
        version:
          description: Installed version.
          returned: always
          type: str
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
    versions:
      description: Available versions of the formula.
      returned: always
      type: dict
      contains:
        bottle:
          description: Whether a bottle is available.
          returned: always
          type: bool
        head:
          description: HEAD version, or V(null) when the formula has no HEAD.
          returned: always
          type: str
        stable:
          description: Latest stable version.
          returned: always
          type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.homebrew import (
    homebrew_argument_spec,
    homebrew_info,
)


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, formulae=homebrew_info(module, "formula"))


if __name__ == "__main__":
    main()
