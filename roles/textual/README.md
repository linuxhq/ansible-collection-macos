# textual

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Textual IRC Client

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    textual_defaults: []
    textual_domain: com.codeux.apps.textual
    textual_package: textual
    textual_state: present

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
