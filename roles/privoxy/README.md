# privoxy

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

A non-caching web proxy

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

Available variables are listed below, along with default values:

    privoxy_accept_intercepted_requests: false
    privoxy_actionsfiles:
      - match-all.action
      - default.action
      - user.action
    privoxy_admin_address: privoxy@localhost
    privoxy_allow_cgi_request_crunching: false
    privoxy_buffer_limit: 4096
    privoxy_client_header_order: []
    privoxy_compression_level: 1
    privoxy_confdir: /opt/homebrew/etc/privoxy
    privoxy_connection_sharing: false
    privoxy_debug:
      - 0
    privoxy_default_server_timeout: 60
    privoxy_deny_access: []
    privoxy_enable_compression: false
    privoxy_enable_edit_actions: false
    privoxy_enable_remote_toggle: false
    privoxy_enable_remote_http_toggle: false
    privoxy_enable_proxy_authentication_forwarding: false
    privoxy_enforce_blocks: false
    privoxy_filterfiles:
      - default.filter
      - user.filter
    privoxy_forward: []
    privoxy_forward_socks4: []
    privoxy_forward_socks4a: []
    privoxy_forward_socks5: []
    privoxy_forward_socks5t: []
    privoxy_forwarded_connect_retries: 0
    privoxy_handle_as_empty_doc_returns_ok: false
    privoxy_hostname: "{{ inventory_hostname }}"
    privoxy_keep_alive_timeout: 5
    privoxy_listen_address: '127.0.0.1:8118'
    privoxy_logdir: /opt/homebrew/var/log/privoxy
    privoxy_logfile: logfile
    privoxy_max_client_connections: 128
    privoxy_permit_access: []
    privoxy_proxy_info_url: http://www.example.com/proxy-service.html
    privoxy_single_threaded: false
    privoxy_split_large_forms: false
    privoxy_socket_timeout: 300
    privoxy_templdir: ''
    privoxy_temporary_directory: ''
    privoxy_toggle: true
    privoxy_tolerate_pipelining: true
    privoxy_trust_info_url: []
    privoxy_trustfile: ''
    privoxy_user_manual: /opt/homebrew/share/doc/privoxy/user-manual

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.privoxy
          privoxy_admin_address: privoxy@linuxhq.org
          privoxy_forward_socks5t:
            - target_pattern: /
              socks_proxy: 127.0.0.1:9050
              http_parent: '.'

## License

Copyright (C) 2023 Linux HeadQuarters

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
