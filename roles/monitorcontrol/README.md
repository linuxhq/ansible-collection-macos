# monitorcontrol

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Control your external monitor brightness, contrast or volume

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

Available variables are listed below, along with default values:

    monitorcontrol_defaults: []
    monitorcontrol_domain: me.guillaumeb.MonitorControl
    monitorcontrol_package: monitorcontrol

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
