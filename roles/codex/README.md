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
    codex_marketplaces: []
    codex_package: codex
    codex_plugins: []
    codex_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.codex
          codex_config:
            approval_policy: never
            check_for_update_on_startup: false
            features:
              hooks: true
              memories: false
            model: gpt-6-astra
            model_reasoning_effort: medium
            notice:
              fast_default_opt_out: true
              hide_rate_limit_model_nudge: true
            plan_mode_reasoning_effort: medium
            projects:
              /Users/admin/molecule:
                trust_level: trusted
            sandbox_mode: danger-full-access
            tui:
              show_tooltips: false
          codex_marketplaces:
            - name: sendbird
              source: https://github.com/sendbird/codex-marketplace.git
              state: present
          codex_plugins:
            # https://github.com/sendbird/cc-plugin-codex
            - marketplace: sendbird
              name: cc
              state: present
