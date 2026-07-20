# homebrew

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Manage homebrew formulae

## Requirements

* [Homebrew](https://brew.sh/)

## Role Variables

    homebrew_list: []
    homebrew_path: null
    homebrew_update: false
    homebrew_upgrade: false
    homebrew_upgrade_options: []

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew_tap
          homebrew_tap_list:
            - name: hashicorp/tap

        - role: linuxhq.macos.homebrew
          homebrew_list:
            - name: cloudflared
            - name: mas
            - name: pyenv
            - name: shellcheck
            - name: hashicorp/tap/vault
