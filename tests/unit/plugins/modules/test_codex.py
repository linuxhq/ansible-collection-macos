"""State transitions and failure contracts for both Codex modules."""

import pytest

from ansible_collections.linuxhq.macos.plugins.modules import codex_marketplace, codex_plugin

SOURCE = "https://github.com/example/codex-marketplace.git"

MARKETPLACE = {
    "name": "example",
    "root": "/home/test/.codex/.tmp/marketplaces/example",
    "marketplaceSource": {"sourceType": "git", "source": SOURCE},
}

MARKETPLACE_RESULT = {
    "name": "example",
    "root": "/home/test/.codex/.tmp/marketplaces/example",
    "marketplace_source": {"source_type": "git", "source": SOURCE},
}

PLUGIN = {
    "pluginId": "editor@example",
    "name": "editor",
    "marketplaceName": "example",
    "version": "1.0.0",
    "installed": True,
    "enabled": True,
    "source": {"source": "local", "path": "/home/test/.codex/.tmp/marketplaces/example/plugins/editor"},
    "marketplaceSource": {"sourceType": "git", "source": SOURCE},
    "installPolicy": "AVAILABLE",
    "authPolicy": "ON_INSTALL",
}

PLUGIN_RESULT = {
    "plugin_id": "editor@example",
    "name": "editor",
    "marketplace_name": "example",
    "version": "1.0.0",
    "installed": True,
    "enabled": True,
    "source": {"source": "local", "path": "/home/test/.codex/.tmp/marketplaces/example/plugins/editor"},
    "marketplace_source": {"source_type": "git", "source": SOURCE},
    "install_policy": "AVAILABLE",
    "auth_policy": "ON_INSTALL",
}


def added(name="example", already_added=False):
    return {
        "marketplaceName": name,
        "installedRoot": f"/home/test/.codex/.tmp/marketplaces/{name}",
        "alreadyAdded": already_added,
    }


def removed(name="example"):
    return {"marketplaceName": name, "installedRoot": None}


@pytest.fixture(params=["marketplace", "plugin"])
def resource(request):
    if request.param == "marketplace":
        return (
            codex_marketplace,
            {"name": "example", "source": SOURCE},
            "marketplaces",
            "marketplace",
            MARKETPLACE,
            MARKETPLACE_RESULT,
            ["plugin", "marketplace"],
            SOURCE,
            "example",
            added(),
        )

    return (
        codex_plugin,
        {"name": "editor", "marketplace": "example"},
        "installed",
        "plugin",
        PLUGIN,
        PLUGIN_RESULT,
        ["plugin"],
        "editor@example",
        "editor@example",
        {
            "pluginId": "editor@example",
            "name": "editor",
            "marketplaceName": "example",
            "version": "1.0.0",
            "installedPath": "/home/test/.codex/plugins/cache/example/editor/1.0.0",
            "authPolicy": "ON_INSTALL",
        },
    )


@pytest.mark.parametrize(
    "state,exists,check_mode,changed",
    [
        ("absent", False, False, False),
        ("present", True, True, False),
        ("absent", False, True, False),
        ("present", False, True, True),
        ("absent", True, True, True),
    ],
)
def test_idempotency_and_check_mode(run_module, resource, state, exists, check_mode, changed):
    plugin, params, key, result_key, item, _expected, prefix, *_details = resource
    result, command, _lookup = run_module(
        plugin, {**params, "state": state}, [{key: [item] if exists else []}], check_mode
    )
    assert result["changed"] is changed
    assert result.get("failed") is None
    assert (result[result_key] is not None) is exists
    assert command.call_count == 1
    assert command.call_args.args[0] == ["/mock/bin/tool", *prefix, "list", "--json"]


def test_existing_plugin_is_unchanged(run_module):
    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "example"}, [{"installed": [PLUGIN]}]
    )
    assert result == {"changed": False, "plugin": PLUGIN_RESULT}
    assert command.call_count == 1


def test_existing_marketplace_with_same_source_is_unchanged(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [MARKETPLACE]}, added(already_added=True)],
    )
    assert result == {"changed": False, "marketplace": MARKETPLACE_RESULT}
    assert command.call_count == 2
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "add", SOURCE, "--json"]


def test_existing_marketplace_with_different_source_fails(run_module):
    stderr = (
        "Error: marketplace 'example' is already added from a different source; remove it before adding this source\n"
    )
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": "/other/source"},
        [{"marketplaces": [MARKETPLACE]}, (1, "", stderr)],
    )
    assert result["failed"] is True
    assert result["msg"] == (
        "Unable to add Codex marketplace example from /other/source: Error: marketplace 'example' is already "
        "added from a different source; remove it before adding this source"
    )
    assert command.call_count == 2


@pytest.mark.parametrize("check_mode", [False, True])
@pytest.mark.parametrize(
    "existing", [{"name": "example", "root": "/home/test"}, {**MARKETPLACE, "marketplaceSource": None}]
)
def test_existing_marketplace_without_source_fails(run_module, check_mode, existing):
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "source": SOURCE}, [{"marketplaces": [existing]}], check_mode
    )
    assert result["failed"] is True
    assert result["msg"] == (f"Codex marketplace example has no configured source and cannot be managed from {SOURCE}.")
    assert command.call_count == 1


def test_new_marketplace_with_different_manifest_name_is_removed(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added("other"), removed("other")],
    )
    assert result["failed"] is True
    assert result["msg"] == f"Codex marketplace source {SOURCE} declares marketplace other, not example."
    assert command.call_count == 3
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "remove", "other", "--json"]


def test_existing_marketplace_with_different_manifest_name_is_kept(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added("other", already_added=True)],
    )
    assert result["failed"] is True
    assert "declares marketplace other, not example" in result["msg"]
    assert command.call_count == 2


@pytest.mark.parametrize(
    "response",
    [{}, {"marketplaceName": None, "alreadyAdded": False}, {"marketplaceName": "example", "alreadyAdded": "no"}],
)
def test_unexpected_marketplace_add_result(run_module, response):
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "source": SOURCE}, [{"marketplaces": []}, response]
    )
    assert result["failed"] is True
    assert result["msg"] == f"Unexpected codex output while add Codex marketplace example from {SOURCE}."
    assert command.call_count == 2


@pytest.mark.parametrize("state", ["present", "absent"])
def test_mutation_refreshes_state(run_module, resource, state):
    plugin, params, key, result_key, item, expected, prefix, add_arg, remove_arg, add_result = resource
    creating = state == "present"
    responses = [
        {key: [] if creating else [item]},
        add_result if creating else {},
        {key: [item] if creating else []},
    ]
    result, command, _lookup = run_module(plugin, {**params, "state": state}, responses)
    assert result["changed"] is True
    assert command.call_count == 3
    assert command.call_args_list[1].args[0] == [
        "/mock/bin/tool",
        *prefix,
        "add" if creating else "remove",
        add_arg if creating else remove_arg,
        "--json",
    ]
    assert result[result_key] == (expected if creating else None)


@pytest.mark.parametrize("state", ["present", "absent"])
def test_failed_postcondition(run_module, resource, state):
    plugin, params, key, _result_key, item, _expected, _prefix, _add, _remove, add_result = resource
    unchanged = [] if state == "present" else [item]
    responses = [{key: unchanged}, add_result if state == "present" else {}, {key: unchanged}]
    result, command, _lookup = run_module(plugin, {**params, "state": state}, responses)
    assert result["failed"] is True
    assert ("not found" if state == "present" else "remains") in result["msg"]
    assert command.call_count == 3


@pytest.mark.parametrize("state", ["present", "absent"])
def test_missing_executable_in_check_mode(run_module, resource, state):
    plugin, params, _key, result_key, *_details = resource
    result, command, _lookup = run_module(plugin, {**params, "state": state}, check_mode=True, executable=None)
    assert result["changed"] is (state == "present")
    assert result[result_key] is None
    assert "not installed" in result["msg"]
    command.assert_not_called()


def test_marketplace_options_preserve_argument_boundaries(run_module):
    params = {
        "name": "example",
        "source": "/repo with spaces",
        "ref": "release branch",
        "sparse": ["plugins/editor", "plugins/with space"],
    }
    result, command, _lookup = run_module(
        codex_marketplace, params, [{"marketplaces": []}, added(), {"marketplaces": [MARKETPLACE]}]
    )
    assert result["changed"] is True
    assert command.call_args_list[1].args[0] == [
        "/mock/bin/tool",
        "plugin",
        "marketplace",
        "add",
        "/repo with spaces",
        "--ref",
        "release branch",
        "--sparse",
        "plugins/editor",
        "--sparse",
        "plugins/with space",
        "--json",
    ]


@pytest.mark.parametrize(
    "plugin,params,message",
    [
        (codex_marketplace, {"name": "example"}, "source"),
        (codex_plugin, {"name": "editor"}, "marketplace"),
        (codex_plugin, {"name": "editor", "marketplace": "example", "state": "invalid"}, "state"),
    ],
)
def test_argument_validation(run_module, plugin, params, message):
    result, command, _lookup = run_module(plugin, params)
    assert result["failed"] is True
    assert message in result["msg"]
    command.assert_not_called()


def test_plugin_lookup_matches_marketplace(run_module):
    result, command, _lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "wanted"},
        [{"installed": [PLUGIN]}],
        check_mode=True,
    )
    assert result["changed"] is True
    assert result["plugin"] is None
    assert command.call_count == 1
