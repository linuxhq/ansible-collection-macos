# sizeup

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

The Missing Window Manager

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    sizeup_defaults: []
    sizeup_domain: com.irradiatedsoftware.SizeUp
    sizeup_package: sizeup
    sizeup_state: present

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
