# homebrew\_cask\_info

[![License](https://img.shields.io/badge/license-GPLv3-lightgreen)](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text)

Gather information about Homebrew casks

## Requirements

* [Homebrew](https://brew.sh)

## Role Variables

    homebrew_cask_info_name: []
    homebrew_cask_info_path: null

## Dependencies

None

## Return Values

    _homebrew_cask_info_dict
    _homebrew_cask_info_list

## Example Playbook

    - hosts: workstation
      connection: local
      roles:
        - role: linuxhq.macos.homebrew_cask
          homebrew_cask_list:
            - name: iterm2
            - name: rectangle

        - role: linuxhq.macos.homebrew_cask_info
          homebrew_cask_info_name:
            - iterm2
            - rectangle
