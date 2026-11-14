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
  - With O(state=present), an existing marketplace is passed to C(codex plugin
    marketplace add) again, and Codex decides whether O(source) matches the
    configured source.
  - The source of an existing marketplace cannot be changed in place; remove
    the marketplace with O(state=absent), then add it from the new source.
author:
  - Taylor Kimball (@tkimball83)
attributes:
  check_mode:
    description: Can run in check mode and return changed status prediction
      without modifying the target. An existing marketplace is reported unchanged
      because check mode cannot verify that O(source) matches its configured
      source. If Codex is not installed, reports a change for O(state=present)
      and no change for O(state=absent) without querying marketplace state.
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
      - When O(source) declares a different name, a marketplace this module just
        added is removed again and the module fails.
      - A marketplace without a configured source, such as a built-in or
        discovered marketplace, cannot be managed with O(state=present).
    required: true
    type: str
  ref:
    description:
      - Git reference to fetch when adding a Git marketplace.
      - Used only when O(state=present).
    type: str
  source:
    description:
      - Local path, GitHub repository, HTTPS Git URL, or SSH Git URL.
      - Required when O(state=present).
      - Must match the configured source of an existing marketplace.
    type: str
  sparse:
    description:
      - Sparse checkout paths for a Git marketplace.
      - Used only when O(state=present).
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


def add_marketplace(module):
    name = module.params["name"]
    source = module.params["source"]
    args = ["plugin", "marketplace", "add", source]
    if module.params["ref"]:
        args += ["--ref", module.params["ref"]]

    for sparse_path in module.params["sparse"] or []:
        args += ["--sparse", sparse_path]

    args.append("--json")

    operation = f"add Codex marketplace {name} from {source}"
    result = codex_run_json(module, args, operation)
    if not isinstance(result.get("marketplaceName"), str) or not isinstance(result.get("alreadyAdded"), bool):
        module.fail_json(msg=f"Unexpected codex output while {operation}.")

    return result


def remove_marketplace(module, name):
    codex_run_json(
        module,
        ["plugin", "marketplace", "remove", name, "--json"],
        f"remove Codex marketplace {name}",
    )


def ensure_present(module, marketplace):
    name = module.params["name"]
    source = module.params["source"]
    if marketplace is not None and not marketplace.get("marketplaceSource"):
        module.fail_json(msg=f"Codex marketplace {name} has no configured source and cannot be managed from {source}.")

    if module.check_mode:
        return marketplace is None, marketplace

    result = add_marketplace(module)
    added_name = result["marketplaceName"]
    if added_name != name:
        if not result["alreadyAdded"]:
            remove_marketplace(module, added_name)

        module.fail_json(msg=f"Codex marketplace source {source} declares marketplace {added_name}, not {name}.")

    if result["alreadyAdded"] and marketplace is not None:
        return False, marketplace

    marketplace = find_marketplace(module)
    if marketplace is None:
        module.fail_json(msg=f"Codex marketplace {name} was not found after adding it.")

    return not result["alreadyAdded"], marketplace


def ensure_absent(module, marketplace):
    if marketplace is None:
        return False, None

    if module.check_mode:
        return True, marketplace

    remove_marketplace(module, module.params["name"])
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
            changed=module.params["state"] == "present",
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
