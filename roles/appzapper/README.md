# appzapper

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The uninstaller Apple forgot

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    appzapper_defaults: []
    appzapper_domain: com.appzapper.AppZapper
    appzapper_package: appzapper
    appzapper_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.appzapper
          appzapper_defaults:
            - key: AppleAppsSafe
              type: bool
              value: true
            - key: DefaultsSet
              type: bool
              value: true
            - key: 'Registration Code'
              type: string
              value: APZP-000-000-000-000
            - key: 'Registration Name'
              type: string
              value: 'Taylor Kimball'
            - key: ZapEffects
              type: bool
              value: true
