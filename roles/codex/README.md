# codex

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Install and configure the OpenAI Codex CLI

## Requirements

* [Homebrew](https://brew.sh)
* [TOML Kit](https://pypi.org/project/tomlkit/)

## Role Variables

    codex_config: {}
    codex_config_path: "{{ ansible_facts.env.HOME }}/.codex/config.toml"
    codex_defaults: []
    codex_domain: com.openai.codex
    codex_package: codex
    codex_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.codex
          codex_config:
            check_for_update_on_startup: false
            model: gpt-6-astra
            projects:
              /Users/tkimball/Git:
                trust_level: trusted
