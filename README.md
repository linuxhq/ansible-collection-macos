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
        monitorcontrol_defaults:
          - key: allScreens
            type: bool
            value: true
        protonvpn_defaults:
          - key: AutoConnect
            type: bool
            value: true

      roles:
        - linuxhq.macos.monitorcontrol
        - linuxhq.macos.protonvpn
