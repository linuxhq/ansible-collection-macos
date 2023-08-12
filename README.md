# linuxhq.macos

A collection of macos roles

# Collection

## Build

    ansible-galaxy collection build

## Install

    ansible-galaxy collection install linuxhq.macos

# Playbook

An example playbook utilizing all roles available in this collection

    - hosts: localhost
      connection: local

      vars:
        protonvpn_defaults:
          - key: AutoConnect
            type: bool
            value: true

      roles:
        - linuxhq.macos.protonvpn
