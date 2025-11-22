# shell\_proxy

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Configure proxies via command line

## Requirements

None

## Role Variables

    shell_proxy_file: "{{ lookup('env', 'HOME') }}/.bash_proxies"
    shell_proxy_ftp: false
    shell_proxy_ftp_hostname: localhost
    shell_proxy_ftp_password: null
    shell_proxy_ftp_port: 8080
    shell_proxy_ftp_protocol: http
    shell_proxy_ftp_username: null
    shell_proxy_http: false
    shell_proxy_http_hostname: localhost
    shell_proxy_http_password: null
    shell_proxy_http_port: 8080
    shell_proxy_http_protocol: http
    shell_proxy_http_username: null
    shell_proxy_https: false
    shell_proxy_https_hostname: localhost
    shell_proxy_https_password: null
    shell_proxy_https_port: 8080
    shell_proxy_https_protocol: http
    shell_proxy_https_username: null
    shell_proxy_noproxy:
      - 127.0.0.1
      - localhost

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.shell_proxy
          shell_proxy_http: true
          shell_proxy_http_password: proxypass
          shell_proxy_http_username: tkimball

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
