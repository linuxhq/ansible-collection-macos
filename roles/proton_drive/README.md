# proton\_drive

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Client for Proton Drive

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    proton_drive_defaults: []
    proton_drive_domain: ch.protonmail.drive
    proton_drive_package: proton-drive
    proton_drive_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.proton_drive
