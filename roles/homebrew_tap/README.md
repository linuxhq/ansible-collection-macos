# homebrew\_tap

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Manage homebrew taps

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_tap_list: []
    homebrew_tap_path: null

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew_tap
          homebrew_tap_list:
            - name: beeftornado/rmtree
            - name: hashicorp/tap
