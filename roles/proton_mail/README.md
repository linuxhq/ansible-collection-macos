# proton\_mail

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Client for Proton Mail

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    proton_mail_defaults: []
    proton_mail_domain: ch.protonmail.desktop
    proton_mail_package: proton-mail
    proton_mail_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.proton_mail
