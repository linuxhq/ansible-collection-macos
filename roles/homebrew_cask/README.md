# homebrew\_cask

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Manage homebrew casks

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_cask_list: []
    homebrew_cask_path: null
    homebrew_cask_sudo_password: null
    homebrew_cask_update: false
    homebrew_cask_upgrade: false
    homebrew_cask_upgrade_greedy: false

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew_cask
          homebrew_cask_list:
            - name: iterm2
            - name: rectangle
