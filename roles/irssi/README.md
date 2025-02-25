# irssi

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Your text mode chatting application since 1999

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    irssi_config_dir: "{{ lookup('env', 'HOME') }}/.irssi"
    irssi_config_file: "{{ irssi_config_dir }}/config"
    irssi_channels:
      - name: '#linuxhq'
        autojoin: 'yes'
        chatnet: linuxhq
    irssi_chatnets:
      linuxhq:
        type: IRC
    irssi_ignores:
      - exception: 'no'
        level: 'CTCPS DCC'
        mask: '*'
    irssi_servers:
      - address: irc.linuxhq.org
        autoconnect: 'yes'
        chatnet: linuxhq
        port: 6697
        ssl_verify: 'yes'
        use_ssl: 'yes'
    irssi_settings:
      core:
        nick: linuxhq
        real_name: Linux HeadQuarters
        user_name: linuxhq
    irssi_scripts: []
    irssi_theme: null

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.irssi
          irssi_settings:
            core:
              nick: tkimball
              real_name: Taylor Kimball
              user_name: tkimball

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
