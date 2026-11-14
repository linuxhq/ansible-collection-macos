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

`codex_defaults` items manage preferences in the `codex_domain` domain with
`community.general.osx_defaults`. Items without `key`, or without `value`
unless `state` is `absent`, are skipped.

    codex_defaults:
      - key: string               # required
        value: any                # required unless state is absent
        type: string              # default: string
        state: present            # present or absent; default: present
        host: string              # optional
        array_add: false          # optional

`codex_marketplaces` items manage marketplaces with
`linuxhq.macos.codex_marketplace`. Present marketplaces are added before
plugins are managed; absent marketplaces are removed after plugins.

    codex_marketplaces:
      - name: string              # required; name declared by the manifest
        source: string            # required when state is present
        ref: string               # optional Git reference
        sparse: []                # optional sparse checkout paths
        state: present            # present or absent; default: present

`codex_plugins` items manage plugins with `linuxhq.macos.codex_plugin`.

    codex_plugins:
      - marketplace: string       # required
        name: string              # required
        state: present            # present or absent; default: present

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
            - name: linuxhq
              source: https://github.com/linuxhq/cc-plugin-codex.git
              state: present
          codex_plugins:
            # https://github.com/linuxhq/cc-plugin-codex
            - marketplace: linuxhq
              name: claude
              state: present
