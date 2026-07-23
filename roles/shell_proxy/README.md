# shell\_proxy

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Configure proxies via command line

## Requirements

None

## Role Variables

    shell_proxy_file: "{{ ansible_facts.env.HOME }}/.bash_proxies"
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
    shell_proxy_state: present

## Dependencies

None

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.shell_proxy
          shell_proxy_ftp: true
          shell_proxy_ftp_hostname: proxy.local
          shell_proxy_ftp_password: p@ss/word
          shell_proxy_ftp_port: 2121
          shell_proxy_ftp_username: user@corp
          shell_proxy_http: true
          shell_proxy_http_hostname: proxy.local
          shell_proxy_http_password: p@ss/word
          shell_proxy_http_port: 8118
          shell_proxy_http_username: user@corp
          shell_proxy_https: true
          shell_proxy_https_hostname: proxy.local
          shell_proxy_https_password: p@ss/word
          shell_proxy_https_port: 8443
          shell_proxy_https_username: user@corp
