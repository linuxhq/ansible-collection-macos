# rclone

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

A command-line program to manage files on cloud storage

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    rclone_conf: []
    rclone_path_bin:
      - /opt/homebrew/bin
      - /usr/local/bin
    rclone_path_conf: "{{ ansible_env.HOME }}/.config/rclone/rclone.conf"
    rclone_mounts: []

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.rclone
          rclone_conf:
            - name: public
              type: http
              url: https://pub.rclone.org

          rclone_mounts:
            - name: org.linuxhq.rclone.public
              remote: 'public:'
              mountpoint: "{{ ansible_env.HOME }}/Volumes/Public"
              flags:
                - --read-only
