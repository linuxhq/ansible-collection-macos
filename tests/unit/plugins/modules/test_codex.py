"""State transitions and failure contracts for both Codex modules."""

import pytest

from ansible_collections.linuxhq.macos.plugins.modules import codex_marketplace, codex_plugin


@pytest.fixture(params=["marketplace", "plugin"])
def resource(request):
    if request.param == "marketplace":
        return (
            codex_marketplace,
            {"name": "example", "source": "https://example.test/repo.git"},
            "marketplaces",
            "marketplace",
            {"name": "example", "sourceType": "git"},
            ["plugin", "marketplace"],
            "https://example.test/repo.git",
            "example",
        )

    return (
        codex_plugin,
        {"name": "editor", "marketplace": "example"},
        "installed",
        "plugin",
        {"pluginId": "editor@example", "isEnabled": True},
        ["plugin"],
        "editor@example",
        "editor@example",
    )


@pytest.mark.parametrize(
    "state,exists,check_mode,changed",
    [
        ("present", True, False, False),
        ("absent", False, False, False),
        ("present", True, True, False),
        ("absent", False, True, False),
        ("present", False, True, True),
        ("absent", True, True, True),
    ],
)
def test_idempotency_and_check_mode(run_module, resource, state, exists, check_mode, changed):
    plugin, params, key, result_key, item, prefix, _add_arg, _remove_arg = resource
    result, command, _lookup = run_module(
        plugin, {**params, "state": state}, [{key: [item] if exists else []}], check_mode
    )
    assert result["changed"] is changed
    assert result.get("failed") is None
    assert (result[result_key] is not None) is exists
    assert command.call_count == 1
    assert command.call_args.args[0] == ["/mock/bin/tool", *prefix, "list", "--json"]


@pytest.mark.parametrize("state", ["present", "absent"])
def test_mutation_refreshes_state(run_module, resource, state):
    plugin, params, key, result_key, item, prefix, add_arg, remove_arg = resource
    creating = state == "present"
    responses = [{key: [] if creating else [item]}, {}, {key: [item] if creating else []}]
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
    if creating:
        expected = (
            {"name": "example", "source_type": "git"}
            if result_key == "marketplace"
            else {"plugin_id": "editor@example", "is_enabled": True}
        )
        assert result[result_key] == expected
    else:
        assert result[result_key] is None


@pytest.mark.parametrize("state", ["present", "absent"])
def test_failed_postcondition(run_module, resource, state):
    plugin, params, key, _result_key, item, *_details = resource
    unchanged = [] if state == "present" else [item]
    result, command, _lookup = run_module(plugin, {**params, "state": state}, [{key: unchanged}, {}, {key: unchanged}])
    assert result["failed"] is True
    assert ("not found" if state == "present" else "remains") in result["msg"]
    assert command.call_count == 3


@pytest.mark.parametrize("state", ["present", "absent"])
def test_missing_executable_in_check_mode(run_module, resource, state):
    plugin, params, _key, result_key, *_details = resource
    result, command, _lookup = run_module(plugin, {**params, "state": state}, check_mode=True, executable=None)
    assert result["changed"] is True
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
        codex_marketplace, params, [{"marketplaces": []}, {}, {"marketplaces": [{"name": "example"}]}]
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
        [{"installed": [{"pluginId": "editor@other"}]}],
        check_mode=True,
    )
    assert result["changed"] is True
    assert result["plugin"] is None
    assert command.call_count == 1
