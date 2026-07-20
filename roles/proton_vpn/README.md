# proton\_vpn

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

VPN client focusing on security

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    proton_vpn_defaults: []
    proton_vpn_domain: ch.protonvpn.mac
    proton_vpn_package: protonvpn
    proton_vpn_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.proton_vpn
          proton_vpn_defaults:
            - key: AutoConnect
              type: bool
              value: true
            - key: ConnectOnDemand
              type: bool
              value: true
            - key: LaunchedBefore
              type: bool
              value: true
            - key: NeagentAppeared
              type: bool
              value: true
            - key: "{{ 'NetShield' + ansible_user_id }}"
              type: int
              value: 2
            - key: RememberLogin
              type: bool
              value: true
            - key: StartMinimized
              type: bool
              value: false
            - key: StartOnBoot
              type: bool
              value: true
            - key: SystemNotifications
              type: bool
              value: true
