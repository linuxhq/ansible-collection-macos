# homebrew\_services\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about Homebrew services

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_services_info_name: []
    homebrew_services_info_path: null

`homebrew_services_info_name` lists the services to gather information
about; `[]` gathers every Homebrew service. Names Homebrew does not know
are omitted.

## Dependencies

None

## Return Values

    _homebrew_services_info_dict  # services keyed by name
    _homebrew_services_info_list  # services as reported by brew services info --json

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew
          homebrew_list:
            - name: cloudflared
            - name: privoxy

        - role: linuxhq.macos.homebrew_services_info
          homebrew_services_info_name:
            - cloudflared
            - privoxy
