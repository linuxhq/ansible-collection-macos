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

```sh
ansible-galaxy collection install linuxhq.macos
```

## Development

With Tox installed, install the pre-commit hook:

```sh
tox run -e pre-commit
```

Tox manages isolated environments under `.tox/`; no environment activation is required.

### Checks

Run the default checks:

```sh
tox
```

Run grouped checks:

```sh
tox run -m format
tox run -m lint
```

Run Ansible sanity tests for a module:

```sh
tox run -e ansible-test -- sanity --python "$(cat .python-version)" plugins/modules/codex_marketplace.py
```

### Molecule

Each role has a Molecule scenario that also serves as an example playbook. Set `MOLECULE_ROLE`
to select a role:

```sh
MOLECULE_ROLE=codex tox run -e molecule -- test -s default
```

Role scenarios run against a disposable [Tart](https://tart.run) macOS
virtual machine with the vagrant driver.

```sh
brew tap cirruslabs/cli
brew trust cirruslabs/cli
brew install cirruslabs/cli/tart
brew tap hashicorp/tap
brew trust hashicorp/tap
brew install hashicorp/tap/hashicorp-vagrant
vagrant plugin install vagrant-tart
```

The host application running Molecule needs the macOS Local Network
permission to reach the virtual machines.

### Changelog and build

```sh
tox run -e changelog -- generate
tox run -e build
```
