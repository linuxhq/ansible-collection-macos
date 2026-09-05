#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: codex_plugin
short_description: Manage Codex plugins
version_added: "1.1.0"
description:
  - Install and remove Codex plugins from configured marketplaces.
  - Plugin state is managed through the Codex CLI.
author:
  - Taylor Kimball (@tkimball83)
attributes:
  check_mode:
    description: Can run in check mode and return changed status prediction
      without modifying the target. If Codex is not installed, reports a potential
      change without querying plugin state.
    support: full
  diff_mode:
    description: Diff mode is not supported.
    support: none
options:
  config_dir:
    description:
      - Codex configuration directory.
      - Sets E(CODEX_HOME) for Codex CLI commands when provided.
    type: path
  executable:
    description:
      - Path to the Codex executable.
      - When omitted, C(codex) is searched for in standard executable paths.
    type: path
  marketplace:
    description:
      - Marketplace containing the plugin.
    required: true
    type: str
  name:
    description:
      - Plugin name.
    required: true
    type: str
  state:
    description:
      - Whether the plugin should be installed.
    choices:
      - absent
      - present
    default: present
    type: str
requirements:
  - codex
"""

EXAMPLES = r"""
- name: Ensure the Sendbird Claude Code plugin is present
  linuxhq.macos.codex_plugin:
    marketplace: sendbird
    name: cc
    state: present

- name: Ensure the Sendbird Claude Code plugin is absent
  linuxhq.macos.codex_plugin:
    marketplace: sendbird
    name: cc
    state: absent
"""

RETURN = r"""
---
plugin:
  description:
    - Codex plugin after the requested state is applied.
    - Returns V(null) when the plugin is absent.
    - Also returns V(null) in check mode when Codex is not installed.
  returned: always
  type: dict
  contains:
    auth_policy:
      description: Authentication policy from the marketplace.
      returned: when plugin exists
      type: str
    enabled:
      description: Whether the plugin is enabled.
      returned: when plugin exists
      type: bool
    install_policy:
      description: Installation policy from the marketplace.
      returned: when plugin exists
      type: str
    installed:
      description: Whether the plugin is installed.
      returned: when plugin exists
      type: bool
    marketplace_name:
      description: Marketplace containing the plugin.
      returned: when plugin exists
      type: str
    name:
      description: Plugin name.
      returned: when plugin exists
      type: str
    plugin_id:
      description: Plugin identifier in C(name@marketplace) format.
      returned: when plugin exists
      type: str
    source:
      description: Plugin source information.
      returned: when plugin exists
      type: dict
      contains:
        id:
          description: Remote plugin source identifier.
          returned: when available
          type: str
        path:
          description: Local plugin source path.
          returned: when available
          type: str
        source:
          description: Plugin source type.
          returned: when available
          type: str
    version:
      description: Installed plugin version.
      returned: when plugin exists
      type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.linuxhq.macos.plugins.module_utils.codex import (
    codex_argument_spec,
    codex_bin,
    codex_list,
    codex_result,
    codex_run_json,
)


def plugins(module):
    return codex_list(
        module,
        ["plugin", "list", "--json"],
        "installed",
        "gather Codex plugin information",
    )


def plugin_id(module):
    return f"{module.params['name']}@{module.params['marketplace']}"


def find_plugin(module):
    identifier = plugin_id(module)
    return next(
        (plugin for plugin in plugins(module) if plugin.get("pluginId") == identifier),
        None,
    )


def ensure_present(module, plugin):
    if plugin is not None:
        return False, plugin

    if module.check_mode:
        return True, None

    identifier = plugin_id(module)
    codex_run_json(
        module,
        ["plugin", "add", identifier, "--json"],
        f"install Codex plugin {identifier}",
    )
    plugin = find_plugin(module)
    if plugin is None:
        module.fail_json(
            msg=f"Codex plugin {identifier} was not found after installing it."
        )

    return True, plugin


def ensure_absent(module, plugin):
    if plugin is None:
        return False, None

    if module.check_mode:
        return True, plugin

    identifier = plugin_id(module)
    codex_run_json(
        module,
        ["plugin", "remove", identifier, "--json"],
        f"remove Codex plugin {identifier}",
    )
    plugin = find_plugin(module)
    if plugin is not None:
        module.fail_json(msg=f"Codex plugin {identifier} remains after removing it.")

    return True, None


def main():
    argument_spec = codex_argument_spec()
    argument_spec.update(
        {
            "marketplace": {"required": True, "type": "str"},
            "name": {"required": True, "type": "str"},
            "state": {
                "choices": ["absent", "present"],
                "default": "present",
                "type": "str",
            },
        }
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    if module.check_mode and codex_bin(module, required=False) is None:
        module.exit_json(
            changed=True,
            msg="Codex is not installed; plugin state cannot be determined in check mode.",
            plugin=None,
        )

    plugin = find_plugin(module)
    if module.params["state"] == "present":
        changed, plugin = ensure_present(module, plugin)
    else:
        changed, plugin = ensure_absent(module, plugin)

    module.exit_json(changed=changed, plugin=codex_result(plugin))


if __name__ == "__main__":
    main()
