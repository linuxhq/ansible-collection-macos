#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: homebrew_services_info
version_added: '1.1.0'
short_description: Gather information about Homebrew services
description:
  - Gather service information from Homebrew.
  - With O(name), gather information about the given services.
  - Names that Homebrew does not know are omitted from the results.
  - Without O(name), gather information about every Homebrew service.
  - Homebrew reports a synthesized definition for any known formula, so a
    service is returned only when Homebrew reports its service file as
    registered or the reported service file exists. Services whose formula is
    not installed or defines no service are omitted.
  - Service information is returned as reported by C(brew services info --json).
author:
  - Taylor Kimball (@tkimball83)
options:
  name:
    description:
      - Service names to gather information about.
      - When omitted, information about all Homebrew services is gathered.
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
- name: Gather information about all Homebrew services
  linuxhq.macos.homebrew_services_info:

- name: Gather information about selected Homebrew services
  linuxhq.macos.homebrew_services_info:
    name:
      - privoxy
"""

RETURN = r"""
---
services:
  description:
    - Homebrew services as reported by C(brew services info --json).
    - Each item is returned unmodified; commonly used keys are listed below.
  returned: always
  type: list
  elements: dict
  contains:
    command:
      description: Command the service runs.
      returned: when the formula service defines a command
      type: str
    exit_code:
      description: Last exit code of the service, or V(null) when launchd
        reports none.
      returned: always
      type: int
    file:
      description:
        - Path to the service file.
        - For a service registered in another launchd domain, such as one
          started with C(sudo), the path Homebrew reports may not exist for
          the querying user.
      returned: always
      type: str
    loaded:
      description: Whether the service is loaded by launchd.
      returned: always
      type: bool
    loaded_file:
      description: Path to the loaded service file, or V(null) when launchd
        does not report it.
      returned: always
      type: str
    name:
      description: Formula name of the service.
      returned: always
      type: str
    pid:
      description: Process ID of the service, or V(null) when the service is
        not running.
      returned: always
      type: int
    registered:
      description: Whether a service file is registered in a launchd domain.
      returned: always
      type: bool
    running:
      description: Whether the service is running.
      returned: always
      type: bool
    schedulable:
      description: Whether the service runs on a schedule.
      returned: always
      type: bool
    service_name:
      description: Launchd label of the service.
      returned: always
      type: str
    status:
      description: Status of the service, such as V(none), V(started),
        V(stopped), V(scheduled), V(error), V(unknown), or V(other).
      returned: always
      type: str
    user:
      description: User the service runs as, or V(null) when no service file
        is registered.
      returned: always
      type: str
"""

import os

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.homebrew import (
    homebrew_argument_spec,
    homebrew_services_info,
)


def services(module):
    return [
        service
        for service in homebrew_services_info(module)
        if service.get("registered") is True or (service.get("file") and os.path.exists(service["file"]))
    ]


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, services=services(module))


if __name__ == "__main__":
    main()
