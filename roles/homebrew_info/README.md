# homebrew\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about Homebrew formulae

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_info_name: []
    homebrew_info_path: null

`homebrew_info_name` lists the formulae to gather information about;
`[]` gathers every installed formula. Names Homebrew does not know are
omitted.

## Dependencies

None

## Return Values

    _homebrew_info_dict  # formulae keyed by name
    _homebrew_info_list  # formulae as reported by brew info --json=v2

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
