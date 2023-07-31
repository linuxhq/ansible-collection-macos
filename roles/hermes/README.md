# hermes

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Pandora Client

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

Available variables are listed below, along with default values:

    hermes_defaults: []
    hermes_domain: com.alexcrichton.Hermes
    hermes_package: hermes

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

## License

Copyright (C) 2023 Linux HeadQuarters

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
