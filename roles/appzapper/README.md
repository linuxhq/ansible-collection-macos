# appzapper

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The uninstaller Apple forgot

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    appzapper_defaults: []
    appzapper_domain: com.appzapper.AppZapper
    appzapper_package: appzapper

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
