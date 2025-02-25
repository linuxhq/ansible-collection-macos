# iterm2

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Terminal Replacement

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    iterm2_defaults: []
    iterm2_domain: com.googlecode.iterm2
    iterm2_package: iterm2

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.iterm2
          iterm2_defaults:
            - key: OnlyWhenMoreTabs
              type: string
              value: 0
            - key: PromptOnQuit
              type: bool
              value: false

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
