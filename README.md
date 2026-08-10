# linuxhq.macos

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)
[![Ansible Galaxy](https://img.shields.io/badge/collection-linuxhq.macos-blue)](https://galaxy.ansible.com/linuxhq/macos)
[![Lint](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/pre-commit.yml)
[![Release](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/release.yml/badge.svg)](https://github.com/linuxhq/ansible-collection-macos/actions/workflows/release.yml)

An Ansible collection of macOS modules, plugins, and roles.

## Requirements

- Python `>= 3.13`
- `ansible-core >= 2.18.0`
- `community.general >= 13.2.0`

## Installation

    ansible-galaxy collection install linuxhq.macos

## Development

    make
    source venv/bin/activate

### Build

    ansible-galaxy collection build

### Changelog

    antsibull-changelog generate

### Lint

    ansible-lint
    yamllint -s .

### Test

Every role includes a Molecule scenario with an example playbook.

## Molecule

Role scenarios run against a disposable [Tart](https://tart.run) macOS
virtual machine with the vagrant driver.

    python3 -m venv venv
    source venv/bin/activate
    venv/bin/pip3 install -r requirements.txt

    brew trust cirruslabs/cli
    brew install cirruslabs/cli/tart
    brew tap hashicorp/tap
    brew trust hashicorp/tap
    brew install hashicorp/tap/hashicorp-vagrant
    vagrant plugin install vagrant-tart

The host application running Molecule needs the macOS Local Network
permission to reach the virtual machines.

## Playbook

An example playbook using roles from this collection:

    - hosts: localhost
      connection: local
      roles:
        - role: linuxhq.macos.adguard
          adguard_defaults:
            - key: PopupBlockerEnabled
              type: bool
              value: true

        - role: linuxhq.macos.appzapper
          appzapper_defaults:
            - key: 'Registration Code'
              type: string
              value: APZP-000-000-000-000
            - key: 'Registration Name'
              type: string
              value: 'Taylor Kimball'

        - role: linuxhq.macos.iterm2
          iterm2_defaults:
            - key: PromptOnQuit
              type: bool
              value: false

        - role: linuxhq.macos.liquidprompt
          liquidprompt_battery_threshold: 50
          liquidprompt_enable_time: true

        - role: linuxhq.macos.monitorcontrol
          monitorcontrol_defaults:
            - key: allScreens
              type: bool
              value: true

        - role: linuxhq.macos.privoxy
          privoxy_forward_socks5t:
            - target_pattern: /
              socks_proxy: 127.0.0.1:9050
              http_parent: '.'

        - role: linuxhq.macos.sizeup
          sizeup_defaults:
            - key: MultiMonitorResizeWindowProportionally
              type: bool
              value: true

        - role: linuxhq.macos.textual
          textual_defaults:
            - key: CopyTextSelectionOnMouseUp
              type: bool
              value: true
