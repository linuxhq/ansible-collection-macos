# textual

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Textual IRC Client

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    textual_defaults: []
    textual_domain: com.codeux.apps.textual
    textual_package: textual

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.textual
          textual_defaults:
            - key: CopyTextSelectionOnMouseUp
              type: bool
              value: true
            - key: InvertSidebarColors
              type: bool
              value: true
            - key: MemberListSortFavorsServerStaff
              type: bool
              value: true
            - key: NickkeyColorHashingComputesRGBValue
              type: bool
              value: true
            - key: RejoinChannelOnLocalKick
              type: bool
              value: true
            - key: ReplyUnignoredExternalCTCPRequests
              type: int
              value: 0
            - key: SUAutomaticallyUpdate
              type: bool
              value: true
            - key: SUEnableAutomaticChecks
              type: bool
              value: true
            - key: ServerListDoubleClickConnectServer
              type: bool
              value: true
            - key: ServerListDoubleClickDisconnectServer
              type: bool
              value: true
            - key: ServerListDoubleClickJoinChannel
              type: bool
              value: true
            - key: ServerListDoubleClickLeaveChannel
              type: bool
              value: true
            - key: TextFieldAutomaticGrammarCheck
              type: bool
              value: false
            - key: TextFieldAutomaticSpellCheck
              type: bool
              value: false

## License

Copyright (c) Linux HeadQuarters

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
