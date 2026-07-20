# monitorcontrol

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Control your external monitor brightness, contrast or volume

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    monitorcontrol_defaults: []
    monitorcontrol_domain: me.guillaumeb.MonitorControl
    monitorcontrol_package: monitorcontrol
    monitorcontrol_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.monitorcontrol
          monitorcontrol_defaults:
            - key: allScreens
              type: bool
              value: true
            - key: appAlreadyLaunched
              type: bool
              value: true
            - key: listenFor
              type: int
              value: 0
            - key: lowerContrast
              type: bool
              value: false
            - key: showContrast
              type: bool
              value: false
