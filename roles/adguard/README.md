# adguard

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The world's most advanced ad blocker

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

Available variables are listed below, along with default values:

    adguard_defaults: []
    adguard_domain: com.adguard.Adguard
    adguard_package: adguard

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.adguard
          adguard_defaults:
            - key: FilteringEnabled
              type: bool
              value: true
            - key: FirstRun
              type: bool
              value: false
            - key: KextAllowed
              type: bool
              value: true
            - key: PopupBlockerEnabled
              type: bool
              value: true
            - key: PrivacyProtectionEnabled
              type: bool
              value: true
            - key: SUHasLaunchedBefore
              type: bool
              value: true
            - key: SafebrowsingEnabled
              type: bool
              value: true
            - key: StartAtLogin
              type: bool
              value: true
            - key: WebOfTrustEnabled
              type: bool
              value: true

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
