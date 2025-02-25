# liquidprompt

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

A useful adaptive prompt for bash & zsh

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    liquidprompt_always_display_values: true
    liquidprompt_battery_threshold: 75
    liquidprompt_dest: "{{ lookup('env', 'HOME') }}"
    liquidprompt_disabled_vcs_path: []
    liquidprompt_display_values_as_percents: false
    liquidprompt_enable_aws_profile: true
    liquidprompt_enable_batt: true
    liquidprompt_enable_bzr: true
    liquidprompt_enable_color: true
    liquidprompt_enable_container: true
    liquidprompt_enable_detached_sessions: true
    liquidprompt_enable_dirstack: false
    liquidprompt_enable_error: true
    liquidprompt_enable_fossil: true
    liquidprompt_enable_fqdn: false
    liquidprompt_enable_git: true
    liquidprompt_enable_hg: true
    liquidprompt_enable_jobs: true
    liquidprompt_enable_kubecontext: false
    liquidprompt_enable_kube_namespace: false
    liquidprompt_enable_load: true
    liquidprompt_enable_node_venv: false
    liquidprompt_enable_perm: true
    liquidprompt_enable_proxy: true
    liquidprompt_enable_ruby_venv: false
    liquidprompt_enable_runtime: false
    liquidprompt_enable_runtime_bell: false
    liquidprompt_enable_scls: true
    liquidprompt_enable_screen_title: false
    liquidprompt_enable_shlvl: true
    liquidprompt_enable_shorten_path: true
    liquidprompt_enable_ssh_colors: false
    liquidprompt_enable_sudo: false
    liquidprompt_enable_svn: true
    liquidprompt_enable_temp: true
    liquidprompt_enable_terraform: false
    liquidprompt_enable_time: false
    liquidprompt_enable_title: true
    liquidprompt_enable_title_command: true
    liquidprompt_enable_vcs_root: false
    liquidprompt_enable_virtualenv: true
    liquidprompt_enable_wifi_strength: false
    liquidprompt_hostname_always: '0'
    liquidprompt_load_threshold: 60
    liquidprompt_path: /opt/homebrew/share/liquidprompt
    liquidprompt_path_character_keep: 3
    liquidprompt_path_keep: 2
    liquidprompt_path_length: 35
    liquidprompt_ps1_file: null
    liquidprompt_runtime_threshold: 2
    liquidprompt_source: []
    liquidprompt_temp_threshold: 60
    liquidprompt_time_analog: false
    liquidprompt_user_always: true

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.liquidprompt
          liquidprompt_battery_threshold: 50
          liquidprompt_enable_time: true

## License

Copyright (C) 2025 Linux HeadQuarters

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
