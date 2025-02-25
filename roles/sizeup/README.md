# sizeup

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The Missing Window Manager

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    sizeup_defaults: []
    sizeup_domain: com.irradiatedsoftware.SizeUp
    sizeup_package: sizeup

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.sizeup
          sizeup_defaults:
            - key: CenterNonResizableWindows
              type: bool
              value: true
            - key: KeepWindowsInBounds
              type: bool
              value: true
            - key: MenuEnabled
              type: bool
              value: true
            - key: MultiMonitorResizeWindowProportionally
              type: bool
              value: true
            - key: SUEnableAutomaticChecks
              type: bool
              value: true
            - key: ShortcutsDisabled
              type: bool
              value: false
            - key: ShowOverlay
              type: bool
              value: true
            - key: ShowPrefsOnLaunch
              type: bool
              value: false
            - key: ShowPrefsOnNextStart
              type: bool
              value: false
            - key: ShowTooltips
              type: bool
              value: false
            - key: TakeDrawersIntoAccount
              type: bool
              value: true
            - key: suppressMenuBarDisabledPopup
              type: bool
              value: true

## License

Copyright (C) 2025 Linux HeadQuarters

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
