# rectangle

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Rectangle is a window management app based on Spectacle, written in Swift

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    rectangle_defaults: []
    rectangle_domain: com.knollsoft.Rectangle
    rectangle_package: rectangle
    rectangle_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.rectangle
          rectangle_defaults:
            - key: SUEnableAutomaticChecks
              type: bool
              value: true
            - key: allowAnyShortcut
              type: bool
              value: true
            - key: launchOnLogin
              type: bool
              value: true
