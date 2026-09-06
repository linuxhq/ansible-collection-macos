#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: codex_marketplace
short_description: Manage Codex plugin marketplaces
version_added: "1.1.0"
description:
  - Add and remove Codex plugin marketplace sources.
  - Marketplace state is managed through the Codex CLI.
author:
  - Taylor Kimball (@tkimball83)
attributes:
  check_mode:
    description: Can run in check mode and return changed status prediction
      without modifying the target. If Codex is not installed, reports a potential
      change without querying marketplace state.
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
  name:
    description:
      - Marketplace name declared by its marketplace manifest.
    required: true
    type: str
  ref:
    description:
      - Git reference to fetch when adding a Git marketplace.
      - Used only when O(state=present) and the marketplace is absent.
    type: str
  source:
    description:
      - Local path, GitHub repository, HTTPS Git URL, or SSH Git URL.
      - Required when O(state=present).
    type: str
  sparse:
    description:
      - Sparse checkout paths for a Git marketplace.
      - Used only when O(state=present) and the marketplace is absent.
    elements: str
    type: list
  state:
    description:
      - Whether the marketplace should be registered.
    choices:
      - absent
      - present
    default: present
    type: str
requirements:
  - codex
"""

EXAMPLES = r"""
- name: Ensure the Sendbird marketplace is present
  linuxhq.macos.codex_marketplace:
    name: sendbird
    source: https://github.com/sendbird/codex-marketplace.git
    state: present

- name: Ensure a sparse marketplace checkout is present
  linuxhq.macos.codex_marketplace:
    name: example
    ref: main
    source: example/codex-marketplace
    sparse:
      - .agents/plugins
    state: present

- name: Ensure the Sendbird marketplace is absent
  linuxhq.macos.codex_marketplace:
    name: sendbird
    state: absent
"""

RETURN = r"""
---
marketplace:
  description:
    - Codex marketplace after the requested state is applied.
    - Returns V(null) when the marketplace is absent.
    - Also returns V(null) in check mode when Codex is not installed.
  returned: always
  type: dict
  contains:
    marketplace_source:
      description: Configured marketplace source.
      returned: when available
      type: dict
      contains:
        source:
          description: Marketplace source location.
          returned: when available
          type: str
        source_type:
          description: Marketplace source type.
          returned: when available
          type: str
    name:
      description: Marketplace name.
      returned: when marketplace exists
      type: str
    root:
      description: Resolved marketplace root directory.
      returned: when marketplace exists
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


def marketplaces(module):
    return codex_list(
        module,
        ["plugin", "marketplace", "list", "--json"],
        "marketplaces",
        "gather Codex marketplace information",
    )


def find_marketplace(module):
    return next(
        (marketplace for marketplace in marketplaces(module) if marketplace.get("name") == module.params["name"]),
        None,
    )


def ensure_present(module, marketplace):
    if marketplace is not None:
        return False, marketplace

    if module.check_mode:
        return True, None

    args = [
        "plugin",
        "marketplace",
        "add",
        module.params["source"],
    ]
    if module.params["ref"]:
        args += ["--ref", module.params["ref"]]

    for sparse_path in module.params["sparse"] or []:
        args += ["--sparse", sparse_path]

    args.append("--json")

    codex_run_json(module, args, f"add Codex marketplace {module.params['name']}")
    marketplace = find_marketplace(module)
    if marketplace is None:
        module.fail_json(msg=f"Codex marketplace {module.params['name']} was not found after adding it.")

    return True, marketplace


def ensure_absent(module, marketplace):
    if marketplace is None:
        return False, None

    if module.check_mode:
        return True, marketplace

    codex_run_json(
        module,
        [
            "plugin",
            "marketplace",
            "remove",
            module.params["name"],
            "--json",
        ],
        f"remove Codex marketplace {module.params['name']}",
    )
    marketplace = find_marketplace(module)
    if marketplace is not None:
        module.fail_json(msg=f"Codex marketplace {module.params['name']} remains after removing it.")

    return True, None


def main():
    argument_spec = codex_argument_spec()
    argument_spec.update(
        {
            "name": {"required": True, "type": "str"},
            "ref": {"type": "str"},
            "source": {"type": "str"},
            "sparse": {"elements": "str", "type": "list"},
            "state": {
                "choices": ["absent", "present"],
                "default": "present",
                "type": "str",
            },
        }
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[("state", "present", ["source"])],
        supports_check_mode=True,
    )

    if module.check_mode and codex_bin(module, required=False) is None:
        module.exit_json(
            changed=True,
            marketplace=None,
            msg="Codex is not installed; marketplace state cannot be determined in check mode.",
        )

    marketplace = find_marketplace(module)
    if module.params["state"] == "present":
        changed, marketplace = ensure_present(module, marketplace)
    else:
        changed, marketplace = ensure_absent(module, marketplace)

    module.exit_json(changed=changed, marketplace=codex_result(marketplace))


if __name__ == "__main__":
    main()
