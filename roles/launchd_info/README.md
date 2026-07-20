# launchd\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about launchd services

## Requirements

None

## Role Variables

    launchd_info_name: []

## Dependencies

None

## Return Values

    _launchd_info_dict
    _launchd_info_list

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.launchd_info
