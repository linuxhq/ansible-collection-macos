# rclone

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

A command-line program to manage files on cloud storage

## Requirements

None

## Role Variables

    rclone_conf: []
    rclone_path_bin: "{{ ansible_env.HOME }}/.local/bin/rclone"
    rclone_path_conf: "{{ ansible_env.HOME }}/.config/rclone/rclone.conf"
    rclone_path_plist: "{{ ansible_env.HOME }}/Library/LaunchAgents"
    rclone_mounts: []
    rclone_version: v1.73.0

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.rclone
          rclone_conf:
            - name: koofr
              password: "{{ rclone_koofr_password }}"
              provider: koofr
              type: koofr
              user: "{{ rclone_koofr_username }}"

            - name: koofr-crypt
              password: "{{ rclone_koofr_crypt_password }}"
              password2: "{{ rclone_koofr_crypt_password2 }}"
              remote: 'koofr:/rclone'
              type: crypt

          rclone_mounts:
            - name: org.linuxhq.rclone.koofr
              remote: 'koofr-crypt:'
              mountpoint: "{{ ansible_env.HOME }}/Volumes/Koofr"
              flags:
                - --read-only

## License

Copyright (c) Linux HeadQuarters

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
