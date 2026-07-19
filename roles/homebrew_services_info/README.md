# homebrew\_services\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about Homebrew services

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_services_info_name: []
    homebrew_services_info_path: null

## Dependencies

None

## Return Values

    _homebrew_services_info_dict
    _homebrew_services_info_list

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew
          homebrew_packages:
            - name: cloudflared
            - name: privoxy

        - role: linuxhq.macos.homebrew_services_info
          homebrew_services_info_name:
            - cloudflared
            - privoxy
