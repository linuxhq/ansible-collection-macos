# adguard

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The world's most advanced ad blocker

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    adguard_defaults: []
    adguard_domain: com.adguard.Adguard
    adguard_package: adguard
    adguard_state: present

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
