#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: launchd_info
short_description: Gather information about launchd services
description:
  - Gather service information from launchd.
  - With O(name), gather information about the given service labels; labels
    that are not loaded are omitted from the results.
  - Without O(name), gather information about every loaded service.
  - Results reflect the launchd session domain of the connecting user.
author:
  - Taylor Kimball (@tkimball83)
options:
  name:
    description:
      - Service labels to gather information about.
      - When omitted, information about all loaded services is gathered.
    elements: str
    type: list
requirements:
  - launchd
"""

EXAMPLES = r"""
- name: Gather information about all loaded launchd services
  linuxhq.macos.launchd_info:

- name: Gather information about selected launchd services
  linuxhq.macos.launchd_info:
    name:
      - org.linuxhq.rclone.public
"""

RETURN = r"""
---
services:
  description: Launchd services.
  returned: always
  type: list
  elements: dict
  contains:
    label:
      description: Service label.
      returned: always
      type: str
    last_exit_status:
      description: Last exit status of the service, or V(null) when the
        service has not exited.
      returned: always
      type: int
    pid:
      description: Process ID of the service, or V(null) when the service is
        not running.
      returned: always
      type: int
    running:
      description: Whether the service is running.
      returned: always
      type: bool
"""

from ansible.module_utils.basic import AnsibleModule


def info(module, launchctl_bin):
    rc, stdout, stderr = module.run_command([launchctl_bin, "list"])
    if rc != 0:
        module.fail_json(
            msg="Unable to gather launchd information: %s" % stderr.strip()
        )

    lines = stdout.splitlines()
    if not lines or lines[0].split("\t") != ["PID", "Status", "Label"]:
        module.fail_json(
            msg="Unexpected launchctl list header: %s" % (lines or [""])[0]
        )

    services = []

    for line in lines[1:]:
        if not line:
            continue

        columns = line.split("\t")
        if len(columns) != 3:
            module.fail_json(msg="Unexpected launchctl list line: %s" % line)

        pid, status, label = columns
        if module.params["name"] and label not in module.params["name"]:
            continue

        services.append(
            {
                "label": label,
                "last_exit_status": int(status) if status not in ("-", "") else None,
                "pid": int(pid) if pid not in ("-", "") else None,
                "running": pid not in ("-", ""),
            }
        )

    return services


def main():
    module = AnsibleModule(
        argument_spec={
            "name": {"elements": "str", "type": "list"},
        },
        supports_check_mode=True,
    )

    launchctl_bin = module.get_bin_path("launchctl", opt_dirs=["/bin"])
    if not launchctl_bin:
        module.fail_json(msg="Unable to locate launchctl executable.")

    module.exit_json(changed=False, services=info(module, launchctl_bin))


if __name__ == "__main__":
    main()
