# claude_code

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Install and configure the Anthropic Claude Code CLI

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    claude_code_config: {}
    claude_code_config_path: "{{ ansible_facts.env.HOME }}/.claude/settings.json"
    claude_code_package: claude-code
    claude_code_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.claude_code
          claude_code_config:
            permissions:
              defaultMode: acceptEdits
            spinnerTipsEnabled: false
