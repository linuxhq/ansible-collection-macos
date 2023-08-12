# linuxhq.macos

[![Ansible Galaxy](https://img.shields.io/badge/collection-linuxhq.macos-blue)](https://galaxy.ansible.com/linuxhq/macos)

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
        appzapper_defaults:
          - key: 'Registration Code'
            type: string
            value: APZP-000-000-000-000
          - key: 'Registration Name'
            type: string
            value: 'Taylor Kimball'
        monitorcontrol_defaults:
          - key: allScreens
            type: bool
            value: true
        protonvpn_defaults:
          - key: AutoConnect
            type: bool
            value: true

      roles:
        - linuxhq.macos.appzapper
        - linuxhq.macos.monitorcontrol
        - linuxhq.macos.protonvpn
