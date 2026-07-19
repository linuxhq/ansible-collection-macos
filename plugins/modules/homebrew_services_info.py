#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: homebrew_services_info
short_description: Gather information about Homebrew services
description:
  - Gather service information from Homebrew.
  - With O(name), gather information about the given services.
  - Without O(name), gather information about every Homebrew service.
  - Services whose formula is not installed are omitted; Homebrew reports a
    synthesized definition for any known formula, which this module filters
    by the existence of the service property list.
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
  description: Homebrew services.
  returned: always
  type: list
  elements: dict
  contains:
    exit_code:
      description: Exit code of the service, or V(null) when the service is
        not loaded.
      returned: always
      type: int
    file:
      description: Path to the service property list file.
      returned: always
      type: str
    loaded:
      description: Whether the service is loaded by launchd.
      returned: always
      type: bool
    name:
      description: Service name.
      returned: always
      type: str
    pid:
      description: Process ID of the service, or V(null) when the service is
        not running.
      returned: always
      type: int
    registered:
      description: Whether the service is registered with Homebrew.
      returned: always
      type: bool
    running:
      description: Whether the service is running.
      returned: always
      type: bool
    status:
      description: Status of the service, such as V(none), V(started), or
        V(error).
      returned: always
      type: str
    user:
      description: User the service runs as, or V(null) when the service is
        not loaded.
      returned: always
      type: str
"""

import os

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.homebrew import (
    homebrew_argument_spec,
    homebrew_services_info,
)


def info(module):
    data = homebrew_services_info(module)

    return [
        {
            "exit_code": service.get("exit_code"),
            "file": service.get("file"),
            "loaded": service.get("loaded", False),
            "name": service.get("name"),
            "pid": service.get("pid"),
            "registered": service.get("registered", False),
            "running": service.get("running", False),
            "status": service.get("status"),
            "user": service.get("user"),
        }
        for service in data
        if service.get("file") and os.path.exists(service["file"])
    ]


def main():
    module = AnsibleModule(
        argument_spec=homebrew_argument_spec(),
        supports_check_mode=True,
    )

    module.exit_json(changed=False, services=info(module))


if __name__ == "__main__":
    main()
