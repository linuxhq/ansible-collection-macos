# iterm2

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Terminal Replacement

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    iterm2_defaults: []
    iterm2_domain: com.googlecode.iterm2
    iterm2_package: iterm2
    iterm2_state: present

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
