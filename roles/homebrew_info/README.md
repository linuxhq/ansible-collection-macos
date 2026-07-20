# homebrew\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about Homebrew formulae

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_info_name: []
    homebrew_info_path: null

## Dependencies

None

## Return Values

    _homebrew_info_dict
    _homebrew_info_list

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew
          homebrew_list:
            - name: cloudflared
            - name: privoxy

        - role: linuxhq.macos.homebrew_info
          homebrew_info_name:
            - cloudflared
            - privoxy
