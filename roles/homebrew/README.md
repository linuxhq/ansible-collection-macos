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

## License

Copyright (c) Linux HeadQuarters

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
