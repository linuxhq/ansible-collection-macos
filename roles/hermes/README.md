# hermes

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Pandora Client

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    hermes_defaults: []
    hermes_domain: com.alexcrichton.Hermes
    hermes_package: hermes
    hermes_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.hermes
          hermes_defaults:
            - key: SUAutomaticallyUpdate
              type: bool
              value: false
            - key: SUHasLaunchedBefore
              type: bool
              value: true
            - key: audioQuality
              type: int
              value: 1
            - key: alwaysOnTop
              type: bool
              value: false
            - key: drawerWidth
              type: int
              value: 130
            - key: openDrawer
              type: int
              value: 0
            - key: pauseOnScreenLock
              type: bool
              value: false
            - key: pauseOnScreensaverStart
              type: bool
              value: false
            - key: playOnScreenUnlock
              type: bool
              value: false
            - key: playOnScreensaverStop
              type: bool
              value: false
            - key: pleaseGrowlPlay
              type: bool
              value: false
            - key: sortStations
              type: int
              value: 2
            - key: statusBarIcon
              type: bool
              value: false
            - key: statusBarIconBlackWhite
              type: bool
              value: false
