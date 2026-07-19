# homebrew

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

A free and open-source package manager for macOS

## Requirements

* [Homebrew](https://brew.sh/)

## Role Variables

    homebrew_casks: []
    homebrew_packages: []
    homebrew_path: null
    homebrew_sudo_password: null
    homebrew_taps: []
    homebrew_update: false
    homebrew_upgrade: false
    homebrew_upgrade_greedy: false
    homebrew_upgrade_options: []

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew
          homebrew_casks:
            - name: docker-desktop
            - name: firefox
            - name: hashicorp-vagrant
            - name: macfuse
            - name: virtualbox

          homebrew_packages:
            - name: cloudflared
            - name: mas
            - name: pyenv
            - name: shellcheck
            - name: vault

          homebrew_taps:
            - name: beeftornado/rmtree
            - name: hashicorp/tap
