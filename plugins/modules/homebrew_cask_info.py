#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: homebrew_cask_info
version_added: '1.1.0'
short_description: Gather information about Homebrew casks
description:
  - Gather cask information from Homebrew.
  - With O(name), gather information about the given casks, whether installed
    or not.
  - Names that Homebrew does not know are omitted from the results.
  - Without O(name), gather information about every installed cask.
  - Cask information is returned as reported by C(brew info --json=v2).
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
attributes:
  check_mode:
    description: This module only retrieves information and does not modify state.
    support: full
  diff_mode:
    description: Diff mode is not supported.
    support: none
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
  description:
    - Homebrew casks as reported by C(brew info --json=v2).
    - Each item is returned unmodified; commonly used keys are listed below.
  returned: always
  type: list
  elements: dict
  contains:
    deprecated:
      description: Whether the cask is deprecated.
      returned: always
      type: bool
    desc:
      description: Short description of the cask.
      returned: always
      type: str
    full_token:
      description: Cask token qualified with its tap when the tap is not
        C(homebrew/cask).
      returned: always
      type: str
    installed:
      description: Installed version of the cask, or V(null) when the cask
        is not installed.
      returned: always
      type: str
    name:
      description: Application names of the cask.
      returned: always
      type: list
      elements: str
    outdated:
      description: Whether the installed cask is outdated.
      returned: always
      type: bool
    tap:
      description: Tap the cask comes from.
      returned: always
      type: str
    token:
      description: Cask token.
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


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, casks=homebrew_info(module, "cask"))


if __name__ == "__main__":
    main()
