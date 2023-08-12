# linuxhq.macos

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)
[![Ansible Galaxy](https://img.shields.io/badge/collection-linuxhq.macos-blue)](https://galaxy.ansible.com/linuxhq/macos)
[![Lint](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/linting.yml/badge.svg)](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/linting.yml)
[![Release](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/release.yml/badge.svg)](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/release.yml)

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
        adguard_defaults:
          - key: PopupBlockerEnabled
            type: bool
            value: true
        appzapper_defaults:
          - key: 'Registration Code'
            type: string
            value: APZP-000-000-000-000
          - key: 'Registration Name'
            type: string
            value: 'Taylor Kimball'
        hermes_defaults:
          - key: statusBarIconBlackWhite
            type: bool
            value: false
        iterm2_defaults:
          - key: PromptOnQuit
            type: bool
            value: false
        liquidprompt_battery_threshold: 50
        liquidprompt_enable_time: true
        monitorcontrol_defaults:
          - key: allScreens
            type: bool
            value: true
        protonvpn_defaults:
          - key: AutoConnect
            type: bool
            value: true
        sizeup_defaults:
          - key: MultiMonitorResizeWindowProportionally
            type: bool
            value: true
        textual_defaults:
          - key: CopyTextSelectionOnMouseUp
            type: bool
            value: true

      roles:
        - linuxhq.macos.adguard
        - linuxhq.macos.appzapper
        - linuxhq.macos.hermes
        - linuxhq.macos.iterm2
        - linuxhq.macos.liquidprompt
        - linuxhq.macos.monitorcontrol
        - linuxhq.macos.protonvpn
        - linuxhq.macos.sizeup
        - linuxhq.macos.textual
