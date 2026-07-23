# irssi

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Your text mode chatting application since 1999

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    irssi_config_dir: "{{ ansible_facts.env.HOME }}/.irssi"
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
    irssi_state: present
    irssi_theme: null

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.irssi
          irssi_channels:
            - name: '#linuxhq'
              autojoin: 'yes'
              chatnet: linuxhq
            - name: '#macos'
              autojoin: 'yes'
              chatnet: oftc
          irssi_chatnets:
            linuxhq:
              type: IRC
            oftc:
              type: IRC
              nick: tkimball
          irssi_ignores:
            - exception: 'no'
              level: 'CTCPS DCC'
              mask: '*'
            - exception: 'no'
              level: 'JOINS PARTS QUITS'
              mask: '#macos'
          irssi_settings:
            core:
              nick: tkimball
              real_name: Taylor Kimball
              user_name: tkimball
