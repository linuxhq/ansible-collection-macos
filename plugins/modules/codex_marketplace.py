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
  - With O(state=present), all marketplaces are listed first with C(codex
    plugin marketplace list), so the module fails while any configured or
    discovered marketplace fails to load. Remove a broken configured
    marketplace with O(state=absent), which does not list marketplaces first.
  - With O(state=present), an existing marketplace is passed to C(codex plugin
    marketplace add) again, and Codex decides whether O(source), O(ref), and
    O(sparse) match the configured marketplace.
  - With O(state=present), a marketplace without a configured source, such as
    a built-in or discovered marketplace, is not treated as present. O(source)
    is passed to C(codex plugin marketplace add), and Codex either adds a
    configured marketplace beside it or rejects the name.
  - Codex replaces an existing local marketplace in place with a Git
    O(source) whose manifest declares the same name.
  - Codex rejects any other change to the O(source), O(ref), or O(sparse) of
    an existing marketplace; remove the marketplace with O(state=absent), then
    add it again with the new values.
  - With O(state=absent), the marketplace is removed with C(codex plugin
    marketplace remove) without listing marketplaces first, so a configured
    marketplace that fails to load can still be removed.
  - With O(state=absent), a marketplace without a configured source, such as
    a built-in or discovered marketplace, is treated as already absent and
    left in place.
  - With O(state=absent), reports no change without running Codex when the
    Codex home directory (O(config_dir), else E(CODEX_HOME), else
    C(~/.codex)) does not exist.
  - Fails before querying or changing marketplace state when C(codex
    --version) reports a version older than 0.153.0.
author:
  - Taylor Kimball (@tkimball83)
attributes:
  check_mode:
    description: Can run in check mode and return changed status prediction
      without modifying the target. An existing configured marketplace is
      reported unchanged because check mode cannot verify that O(source)
      matches its configured source. With O(state=present), a marketplace
      without a configured source, such as a built-in or discovered
      marketplace, is reported as a change. If Codex is not installed or the
      Codex home directory (O(config_dir), else E(CODEX_HOME), else
      C(~/.codex)) does not exist,
      reports a change for O(state=present) and no change for O(state=absent)
      without querying marketplace state. With O(state=absent), reports a
      change without listing marketplaces when the installed marketplace
      directory C(.tmp/marketplaces/<name>) exists in the Codex home
      directory, because Codex removes it even when no marketplace is
      configured. Otherwise, with O(state=absent), reports a change when Codex
      fails to list marketplaces because O(name) fails to load, and fails when
      another marketplace fails to load. Check mode
      cannot see marketplaces while Codex plugins are disabled
      (C(features.plugins)).
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
      - When O(source) declares a different name, the module fails. A
        marketplace this module just added is removed again when Codex lists
        it, while an existing marketplace with the declared name is kept.
    required: true
    type: str
  ref:
    description:
      - Git reference to fetch when adding a Git marketplace.
      - Used only when O(state=present).
      - Must match the configured reference of an existing Git marketplace.
    type: str
  source:
    description:
      - Local path, GitHub repository, HTTPS Git URL, or SSH Git URL.
      - Passed to Codex as given. Codex expands a leading C(~/) in a local
        path; environment variables and C(~user/) are not expanded.
      - Required when O(state=present).
      - Must match the configured source of an existing marketplace, unless a
        Git source replaces a local marketplace.
    type: str
  sparse:
    description:
      - Sparse checkout paths for a Git marketplace.
      - Used only when O(state=present).
      - Must match the configured sparse checkout paths of an existing Git
        marketplace.
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
  - codex >= 0.153.0
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
    - Also returns V(null) in check mode when Codex is not installed or the
      Codex home directory does not exist.
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

import os

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.linuxhq.macos.plugins.module_utils.codex import (
    codex_argument_spec,
    codex_bin,
    codex_home,
    codex_list,
    codex_result,
    codex_run_json,
    codex_unavailable,
    codex_version_check,
)


def marketplaces(module, missing=None):
    return codex_list(
        module,
        ["plugin", "marketplace", "list", "--json"],
        "marketplaces",
        "gather Codex marketplace information",
        missing,
    )


def select_marketplace(listed, name):
    # Codex lists a discovered marketplace before a configured one with the same name.
    matches = [marketplace for marketplace in listed if marketplace["name"] == name]
    return next(
        (marketplace for marketplace in matches if marketplace.get("marketplaceSource")), next(iter(matches), None)
    )


def find_listed(module, name):
    return select_marketplace(marketplaces(module), name)


def find_marketplace(module):
    return find_listed(module, module.params["name"])


def add_marketplace(module):
    name = module.params["name"]
    source = module.params["source"]
    args = ["plugin", "marketplace", "add", "--json"]
    if module.params["ref"]:
        args += ["--ref", module.params["ref"]]

    for sparse_path in module.params["sparse"] or []:
        args += ["--sparse", sparse_path]

    # Codex would parse a source that starts with "-" as an option.
    args += ["--", source]

    return codex_run_json(module, args, f"add Codex marketplace {name} from {source}")


def remove_marketplace(module, name, missing=None):
    return codex_run_json(
        module,
        ["plugin", "marketplace", "remove", "--json", "--", name],
        f"remove Codex marketplace {name}",
        missing,
    )


def ensure_present(module, listed):
    name = module.params["name"]
    source = module.params["source"]
    marketplace = select_marketplace(listed, name)
    # Codex adds a configured marketplace beside a built-in or discovered one with the same name, or rejects it.
    if marketplace is not None and not marketplace.get("marketplaceSource"):
        marketplace = None

    if module.check_mode:
        return marketplace is None, marketplace

    result = add_marketplace(module)
    added_name = result["marketplaceName"]
    if added_name != name:
        msg = f"Codex marketplace source {source} declares marketplace {added_name}, not {name}."
        if not result["alreadyAdded"]:
            # Codex replaces a configured marketplace in place but adds a new entry beside a discovered one.
            replaced = select_marketplace(listed, added_name)
            if replaced is not None and replaced.get("marketplaceSource"):
                module.fail_json(changed=True, msg=f"{msg} Codex replaced the existing marketplace {added_name}.")

            # An unlisted marketplace may be an existing one Codex replaced while plugins are disabled.
            if find_listed(module, added_name) is None:
                module.fail_json(
                    changed=True,
                    msg=f"{msg} Codex added marketplace {added_name} but does not list it, so it was not removed; "
                    "Codex plugins may be disabled (features.plugins).",
                )

            remove_marketplace(module, added_name)

        module.fail_json(msg=msg)

    if result["alreadyAdded"] and marketplace is not None:
        return False, marketplace

    marketplace = find_marketplace(module)
    if marketplace is None:
        module.fail_json(
            changed=not result["alreadyAdded"],
            msg=f"Codex marketplace {name} was added but is not listed by Codex; Codex plugins may be disabled "
            "(features.plugins).",
        )

    return not result["alreadyAdded"], marketplace


def ensure_absent(module):
    name = module.params["name"]
    # Codex removes an installed marketplace directory even when no marketplace is configured or listed.
    if module.check_mode and os.path.exists(os.path.join(codex_home(module), ".tmp", "marketplaces", name)):
        return True, None

    if module.check_mode:
        # Listing fails while any marketplace is broken; removal still succeeds when Codex names this one.
        listed = marketplaces(module, missing=f"\n- `{name}` at ")
        if listed is None:
            return True, None

        # A listed marketplace without a configured source (built-in or discovered) is already absent.
        marketplace = select_marketplace(listed, name)
        return marketplace is not None and bool(marketplace.get("marketplaceSource")), None

    # Remove directly: listing fails while any configured marketplace is broken.
    removed = remove_marketplace(module, name, missing=f"marketplace `{name}` is not configured or installed")
    return removed is not None, None


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

    absent = module.params["state"] == "absent"
    if absent and not module.check_mode:
        # Removal still requires Codex, but a missing Codex home holds nothing to remove.
        codex_bin(module)

    unavailable = (module.check_mode or absent) and codex_unavailable(module)
    if unavailable:
        reason = (
            "marketplace state cannot be determined in check mode" if module.check_mode else "marketplace is absent"
        )
        module.exit_json(changed=not absent, msg=f"{unavailable}; {reason}.", marketplace=None)

    codex_version_check(module)
    if module.params["state"] == "present":
        changed, marketplace = ensure_present(module, marketplaces(module))
    else:
        changed, marketplace = ensure_absent(module)

    module.exit_json(changed=changed, marketplace=codex_result(marketplace))


if __name__ == "__main__":
    main()
