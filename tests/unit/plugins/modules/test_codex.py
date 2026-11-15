"""State transitions and failure contracts for both Codex modules."""

import shutil

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


LIST_ARGS = {
    codex_marketplace: ["plugin", "marketplace", "list", "--json"],
    codex_plugin: ["plugin", "list", "--marketplace", "example", "--json"],
}

NOT_CONFIGURED = (1, "", "Error: marketplace `example` is not configured or installed\n")

DISCOVERED = {"name": "example", "root": "/home/test/.agents/plugins"}


@pytest.mark.parametrize(
    "state,exists,check_mode,changed",
    [
        ("present", True, True, False),
        ("absent", False, True, False),
        ("present", False, True, True),
        ("absent", True, True, True),
    ],
)
def test_idempotency_and_check_mode(run_module, resource, state, exists, check_mode, changed):
    plugin, params, key, result_key, item, *_details = resource
    result, command, _lookup = run_module(
        plugin, {**params, "state": state}, [{key: [item] if exists else []}], check_mode
    )
    assert result["changed"] is changed
    assert result.get("failed") is None
    assert (result[result_key] is not None) is (exists and state == "present")
    assert command.call_count == 2
    assert command.call_args.args[0] == ["/mock/bin/tool", *LIST_ARGS[plugin]]


def test_absent_plugin_is_unchanged(run_module):
    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "example", "state": "absent"}, [{"installed": []}]
    )
    assert result == {"changed": False, "plugin": None}
    assert command.call_count == 2


def test_plugin_list_is_scoped_to_marketplace(run_module):
    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "openai-curated"}, [{"installed": []}], check_mode=True
    )
    assert result["changed"] is True
    assert command.call_args.args[0] == [
        "/mock/bin/tool",
        "plugin",
        "list",
        "--marketplace",
        "openai-curated",
        "--json",
    ]


def test_absent_marketplace_removes_without_listing(run_module):
    result, command, _lookup = run_module(codex_marketplace, {"name": "example", "state": "absent"}, [removed()])
    assert result == {"changed": True, "marketplace": None}
    assert command.call_count == 2
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "remove", "example", "--json"]


@pytest.mark.parametrize(
    "check_mode,responses",
    [
        (False, [NOT_CONFIGURED]),
        (True, [{"marketplaces": []}]),
        (True, [{"marketplaces": [DISCOVERED]}]),
    ],
)
def test_absent_marketplace_not_configured_or_without_source_is_unchanged(run_module, check_mode, responses):
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, responses, check_mode
    )
    assert result == {"changed": False, "marketplace": None}
    assert command.call_count == 2


@pytest.mark.parametrize(
    "response,message",
    [
        ((1, "", "Error: permission denied\n"), "Unable to remove Codex marketplace example: Error: permission denied"),
        ({}, "Unexpected codex output while remove Codex marketplace example."),
        (removed("other"), "Unexpected codex output while remove Codex marketplace example."),
    ],
)
def test_absent_marketplace_remove_failure(run_module, response, message):
    result, command, _lookup = run_module(codex_marketplace, {"name": "example", "state": "absent"}, [response])
    assert result == {"failed": True, "msg": message}
    assert command.call_count == 2


def test_existing_plugin_is_unchanged(run_module):
    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "example"}, [{"installed": [PLUGIN]}]
    )
    assert result == {"changed": False, "plugin": PLUGIN_RESULT}
    assert command.call_count == 2


def test_existing_marketplace_with_same_source_is_unchanged(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [MARKETPLACE]}, added(already_added=True)],
    )
    assert result == {"changed": False, "marketplace": MARKETPLACE_RESULT}
    assert command.call_count == 3
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "add", SOURCE, "--json"]


@pytest.mark.parametrize(
    "check_mode,responses,changed",
    [
        (True, [], False),
        (False, [added(already_added=True)], False),
        (False, [added(), {"marketplaces": [DISCOVERED, MARKETPLACE]}], True),
    ],
)
def test_configured_marketplace_beside_discovered_marketplace_is_managed(run_module, check_mode, responses, changed):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [DISCOVERED, MARKETPLACE]}, *responses],
        check_mode,
    )
    assert result == {"changed": changed, "marketplace": MARKETPLACE_RESULT}
    assert command.call_count == 2 + len(responses)


def test_absent_configured_marketplace_beside_discovered_marketplace_in_check_mode(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "state": "absent"},
        [{"marketplaces": [DISCOVERED, MARKETPLACE]}],
        check_mode=True,
    )
    assert result == {"changed": True, "marketplace": None}
    assert command.call_count == 2


def unloadable(*names):
    issues = "".join(
        f"- `{name}` at /missing/{name}: marketplace root does not contain a supported manifest\n" for name in names
    )
    return 1, "", f"Error: failed to load marketplace(s):\n{issues}"


@pytest.mark.parametrize("names", [["example"], ["other", "example"]])
def test_absent_unloadable_marketplace_in_check_mode_predicts_removal(run_module, names):
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, [unloadable(*names)], check_mode=True
    )
    assert result == {"changed": True, "marketplace": None}
    assert command.call_count == 2


@pytest.mark.parametrize("names", [["other"], ["example2"]])
def test_absent_marketplace_in_check_mode_fails_when_another_is_unloadable(run_module, names):
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, [unloadable(*names)], check_mode=True
    )
    assert result["failed"] is True
    assert result["msg"].startswith("Unable to gather Codex marketplace information: Error: failed to load")
    assert command.call_count == 2


@pytest.mark.parametrize("listed", [{"marketplaces": []}, {"marketplaces": [DISCOVERED]}, unloadable("other")])
def test_absent_installed_marketplace_root_in_check_mode_predicts_removal(run_module, codex_home, listed):
    (codex_home / ".tmp" / "marketplaces" / "example").mkdir(parents=True)
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, [listed], check_mode=True
    )
    assert result == {"changed": True, "marketplace": None}
    command.assert_called_once()
    assert command.call_args.args[0] == ["/mock/bin/tool", "--version"]


def test_absent_installed_marketplace_root_in_check_mode_requires_supported_codex(run_module, codex_home):
    (codex_home / ".tmp" / "marketplaces" / "example").mkdir(parents=True)
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, check_mode=True, version="codex-cli 0.152.0\n"
    )
    assert result == {"failed": True, "msg": "Codex 0.152.0 is installed, but codex >= 0.153.0 is required."}
    command.assert_called_once()
    assert command.call_args.args[0] == ["/mock/bin/tool", "--version"]


def test_absent_other_installed_marketplace_root_in_check_mode_is_unchanged(run_module, codex_home):
    (codex_home / ".tmp" / "marketplaces" / "other").mkdir(parents=True)
    result, command, _lookup = run_module(
        codex_marketplace, {"name": "example", "state": "absent"}, [{"marketplaces": []}], check_mode=True
    )
    assert result == {"changed": False, "marketplace": None}
    assert command.call_count == 2


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
    assert command.call_count == 3


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
    assert command.call_count == 2


def test_new_marketplace_with_different_manifest_name_is_removed(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added("other"), {"marketplaces": [{**MARKETPLACE, "name": "other"}]}, removed("other")],
    )
    assert result["failed"] is True
    assert result["msg"] == f"Codex marketplace source {SOURCE} declares marketplace other, not example."
    assert command.call_count == 5
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "remove", "other", "--json"]


def test_replaced_marketplace_with_different_manifest_name_is_kept(run_module):
    listed = {
        **MARKETPLACE,
        "name": "other",
        "marketplaceSource": {"sourceType": "local", "source": "/home/test/other"},
    }
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [listed]}, added("other")],
    )
    assert result["failed"] is True
    assert result["changed"] is True
    assert result["msg"] == (
        f"Codex marketplace source {SOURCE} declares marketplace other, not example. "
        "Codex replaced the existing marketplace other."
    )
    assert command.call_count == 3


def test_new_marketplace_beside_discovered_marketplace_is_removed(run_module):
    discovered = {"name": "other", "root": "/home/test/.agents/plugins"}
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [discovered]}, added("other"), {"marketplaces": [discovered]}, removed("other")],
    )
    assert result["failed"] is True
    assert "changed" not in result
    assert result["msg"] == f"Codex marketplace source {SOURCE} declares marketplace other, not example."
    assert command.call_count == 5
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "remove", "other", "--json"]


def test_replaced_marketplace_beside_discovered_marketplace_is_kept(run_module):
    configured = {**MARKETPLACE, "name": "other"}
    discovered = {"name": "other", "root": "/home/test/.agents/plugins"}
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": [discovered, configured]}, added("other")],
    )
    assert result["failed"] is True
    assert result["changed"] is True
    assert result["msg"].endswith("Codex replaced the existing marketplace other.")
    assert command.call_count == 3


def test_unlisted_marketplace_with_different_manifest_name_is_kept(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added("other"), {"marketplaces": []}],
    )
    assert result == {
        "changed": True,
        "failed": True,
        "msg": f"Codex marketplace source {SOURCE} declares marketplace other, not example. Codex added marketplace "
        "other but does not list it, so it was not removed; Codex plugins may be disabled (features.plugins).",
    }
    assert command.call_count == 4
    assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "marketplace", "list", "--json"]


def test_existing_marketplace_with_different_manifest_name_is_kept(run_module):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added("other", already_added=True)],
    )
    assert result["failed"] is True
    assert "declares marketplace other, not example" in result["msg"]
    assert command.call_count == 3


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
    assert command.call_count == 3


def test_mutation_refreshes_state(run_module, resource):
    plugin, params, key, result_key, item, expected, prefix, add_arg, _remove_arg, add_result = resource
    responses = [{key: []}, add_result, {key: [item]}]
    result, command, _lookup = run_module(plugin, {**params, "state": "present"}, responses)
    assert result == {"changed": True, result_key: expected}
    assert command.call_count == 4
    assert command.call_args_list[2].args[0] == ["/mock/bin/tool", *prefix, "add", add_arg, "--json"]


def test_plugin_removal_refreshes_state(run_module):
    params = {"name": "editor", "marketplace": "example", "state": "absent"}
    result, command, _lookup = run_module(codex_plugin, params, [{"installed": [PLUGIN]}, {}, {"installed": []}])
    assert result == {"changed": True, "plugin": None}
    assert command.call_count == 4
    assert command.call_args_list[2].args[0] == ["/mock/bin/tool", "plugin", "remove", "editor@example", "--json"]


def test_failed_postcondition(run_module, resource):
    plugin, params, key, _result_key, _item, _expected, _prefix, _add, _remove, add_result = resource
    result, command, _lookup = run_module(plugin, {**params, "state": "present"}, [{key: []}, add_result, {key: []}])
    assert result["failed"] is True
    assert "not found" in result["msg"] or "not listed" in result["msg"]
    assert command.call_count == 4


BROKEN_MARKETPLACE = (
    1,
    "",
    "Error: failed to load configured marketplace snapshot(s):\n- `example` at /missing: no supported manifest\n",
)


@pytest.mark.parametrize("listed", [{"installed": []}, BROKEN_MARKETPLACE])
@pytest.mark.parametrize("check_mode", [False, True])
def test_unlisted_plugin_with_cache_is_removed(run_module, codex_home, check_mode, listed):
    cache = codex_home / "plugins" / "cache" / "example" / "editor"
    (cache / "1.0.0").mkdir(parents=True)

    def remove(args, **_kwargs):
        shutil.rmtree(cache)
        return {}

    params = {"name": "editor", "marketplace": "example", "state": "absent"}
    result, command, _lookup = run_module(codex_plugin, params, [listed, remove], check_mode)
    assert result == {"changed": True, "plugin": None}
    assert cache.is_dir() is check_mode
    if check_mode:
        assert command.call_count == 2
    else:
        assert command.call_count == 3
        assert command.call_args.args[0] == ["/mock/bin/tool", "plugin", "remove", "editor@example", "--json"]


def test_unlisted_plugin_cache_postcondition(run_module, codex_home):
    cache = codex_home / "plugins" / "cache" / "example" / "editor"
    cache.mkdir(parents=True)
    params = {"name": "editor", "marketplace": "example", "state": "absent"}
    result, command, _lookup = run_module(codex_plugin, params, [{"installed": []}, {}])
    assert result == {"failed": True, "msg": f"Codex plugin editor@example remains in {cache} after removing it."}
    assert command.call_args_list[2].args[0] == ["/mock/bin/tool", "plugin", "remove", "editor@example", "--json"]


@pytest.mark.parametrize("listed", [{"installed": []}, BROKEN_MARKETPLACE])
@pytest.mark.parametrize("check_mode", [False, True])
def test_unlisted_plugin_without_cache_is_unchanged(run_module, codex_home, check_mode, listed):
    (codex_home / "plugins" / "cache" / "example" / "other").mkdir(parents=True)
    params = {"name": "editor", "marketplace": "example", "state": "absent"}
    result, command, _lookup = run_module(codex_plugin, params, [listed], check_mode)
    assert result == {"changed": False, "plugin": None}
    assert command.call_count == 2


def test_present_plugin_in_broken_marketplace_fails(run_module, codex_home):
    params = {"name": "editor", "marketplace": "example", "state": "present"}
    result, command, _lookup = run_module(codex_plugin, params, [BROKEN_MARKETPLACE])
    assert result["failed"] is True
    assert result["msg"].startswith("Unable to gather Codex plugin information for marketplace example: Error: failed")
    assert command.call_count == 2


def test_plugin_removal_postcondition(run_module):
    params = {"name": "editor", "marketplace": "example", "state": "absent"}
    result, command, _lookup = run_module(codex_plugin, params, [{"installed": [PLUGIN]}, {}, {"installed": [PLUGIN]}])
    assert result["failed"] is True
    assert "remains" in result["msg"]
    assert command.call_count == 4


@pytest.mark.parametrize("state", ["present", "absent"])
def test_missing_executable_in_check_mode(run_module, resource, state):
    plugin, params, _key, result_key, *_details = resource
    result, command, _lookup = run_module(plugin, {**params, "state": state}, check_mode=True, executable=None)
    assert result["changed"] is (state == "present")
    assert result[result_key] is None
    assert "not installed" in result["msg"]
    command.assert_not_called()


@pytest.mark.parametrize("state", ["present", "absent"])
def test_missing_config_dir_in_check_mode(run_module, resource, tmp_path, state):
    plugin, params, _key, result_key, *_details = resource
    config = str(tmp_path / "missing")
    result, command, _lookup = run_module(plugin, {**params, "state": state, "config_dir": config}, check_mode=True)
    assert result["changed"] is (state == "present")
    assert result[result_key] is None
    assert result["msg"].startswith(f"Codex home directory {config} does not exist;")
    command.assert_not_called()


def test_missing_config_dir_absent(run_module, resource, tmp_path):
    plugin, params, _key, result_key, *_details = resource
    config = str(tmp_path / "missing")
    result, command, _lookup = run_module(plugin, {**params, "state": "absent", "config_dir": config})
    assert result["changed"] is False
    assert result.get("failed") is None
    assert result[result_key] is None
    assert result["msg"] == f"Codex home directory {config} does not exist; {result_key} is absent."
    command.assert_not_called()


def test_missing_executable_absent_fails(run_module, resource, tmp_path):
    plugin, params, *_details = resource
    config = str(tmp_path / "missing")
    params = {**params, "state": "absent", "config_dir": config}
    result, command, _lookup = run_module(plugin, params, executable=None)
    assert result == {"failed": True, "msg": "Unable to locate codex executable."}
    command.assert_not_called()


def test_missing_config_dir_present_runs_codex(run_module, resource, tmp_path):
    plugin, params, *_details = resource
    config = str(tmp_path / "missing")
    error = (1, "", f"Error: CODEX_HOME points to {config}, but that path does not exist\n")
    result, command, _lookup = run_module(plugin, {**params, "config_dir": config}, [error])
    assert result["failed"] is True
    assert "does not exist" in result["msg"]
    assert command.call_count == 2


@pytest.mark.parametrize("environment", ["codex_home", "default"])
@pytest.mark.parametrize("state", ["present", "absent"])
def test_missing_codex_home_in_check_mode(run_module, resource, monkeypatch, tmp_path, environment, state):
    plugin, params, _key, result_key, *_details = resource
    monkeypatch.setenv("HOME", str(tmp_path))
    if environment == "codex_home":
        home = str(tmp_path / "missing")
        monkeypatch.setenv("CODEX_HOME", home)
    else:
        home = str(tmp_path / ".codex")
        monkeypatch.delenv("CODEX_HOME")

    result, command, _lookup = run_module(plugin, {**params, "state": state}, check_mode=True)
    assert result["changed"] is (state == "present")
    assert result[result_key] is None
    assert result["msg"].startswith(f"Codex home directory {home} does not exist;")
    command.assert_not_called()


def test_existing_config_dir_in_check_mode_queries_state(run_module, resource, tmp_path):
    plugin, params, key, _result_key, item, *_details = resource
    result, command, _lookup = run_module(plugin, {**params, "config_dir": str(tmp_path)}, [{key: [item]}], True)
    assert result["changed"] is False
    assert command.call_count == 2
    assert command.call_args.kwargs == {"environ_update": {"CODEX_HOME": str(tmp_path)}}


@pytest.mark.parametrize("already_added", [True, False])
def test_marketplace_added_but_not_listed_names_plugins_feature(run_module, already_added):
    result, command, _lookup = run_module(
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        [{"marketplaces": []}, added(already_added=already_added), {"marketplaces": []}],
    )
    assert result == {
        "changed": not already_added,
        "failed": True,
        "msg": "Codex marketplace example was added but is not listed by Codex; Codex plugins may be disabled "
        "(features.plugins).",
    }
    assert command.call_count == 4


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
    assert command.call_args_list[2].args[0] == [
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
    assert command.call_count == 2


VERSION_ARGS = ["/mock/bin/tool", "--version"]

# A Codex-running path per module, state, and mode, with its responses after the version check.
VERSION_PATHS = [
    (
        codex_marketplace,
        {"name": "example", "source": SOURCE},
        False,
        [{"marketplaces": [MARKETPLACE]}, added(already_added=True)],
    ),
    (codex_marketplace, {"name": "example", "source": SOURCE}, True, [{"marketplaces": [MARKETPLACE]}]),
    (codex_marketplace, {"name": "example", "state": "absent"}, False, [NOT_CONFIGURED]),
    (codex_marketplace, {"name": "example", "state": "absent"}, True, [{"marketplaces": []}]),
    (codex_plugin, {"name": "editor", "marketplace": "example"}, False, [{"installed": [PLUGIN]}]),
    (codex_plugin, {"name": "editor", "marketplace": "example"}, True, [{"installed": [PLUGIN]}]),
    (codex_plugin, {"name": "editor", "marketplace": "example", "state": "absent"}, False, [{"installed": []}]),
    (codex_plugin, {"name": "editor", "marketplace": "example", "state": "absent"}, True, [{"installed": []}]),
]


@pytest.mark.parametrize("plugin,params,check_mode,responses", VERSION_PATHS)
@pytest.mark.parametrize("version", ["codex-cli 0.152.9\n", "codex-cli 0.153.0-alpha.6\n", "codex-cli 0.9.0\n"])
def test_older_codex_fails_before_other_commands(run_module, plugin, params, check_mode, responses, version):
    result, command, _lookup = run_module(plugin, params, responses, check_mode, version=version)
    found = version.split()[1]
    assert result == {"failed": True, "msg": f"Codex {found} is installed, but codex >= 0.153.0 is required."}
    command.assert_called_once()
    assert command.call_args.args[0] == VERSION_ARGS


@pytest.mark.parametrize("plugin,params,check_mode,responses", VERSION_PATHS)
@pytest.mark.parametrize(
    "version", ["codex-cli 0.153.0\n", "codex-cli 0.153.1\n", "codex-cli 0.169.0-alpha.11.1\n", "codex-cli 1.0.0\n"]
)
def test_supported_codex_runs_commands(run_module, plugin, params, check_mode, responses, version):
    result, command, _lookup = run_module(plugin, params, responses, check_mode, version=version)
    assert result.get("failed") is None
    assert command.call_count == 1 + len(responses)
    assert command.call_args_list[0].args[0] == VERSION_ARGS


@pytest.mark.parametrize(
    "version,message",
    [
        ((0, "codex 0.163.0\n", ""), "Unable to parse Codex version from codex --version output: codex 0.163.0"),
        ((0, "", ""), "Unable to parse Codex version from codex --version output: "),
        ((0, "codex-cli 0.163\n", ""), "Unable to parse Codex version from codex --version output: codex-cli 0.163"),
        ((1, "", "Error: unexpected argument\n"), "Unable to determine Codex version: Error: unexpected argument"),
    ],
)
@pytest.mark.parametrize("plugin,params,check_mode,responses", VERSION_PATHS[::2])
def test_unknown_codex_version_fails(run_module, plugin, params, check_mode, responses, version, message):
    result, command, _lookup = run_module(plugin, params, responses, check_mode, version=version)
    assert result == {"failed": True, "msg": message}
    command.assert_called_once()
    assert command.call_args.args[0] == VERSION_ARGS


def test_version_check_uses_config_dir(run_module, tmp_path):
    params = {"name": "editor", "marketplace": "example", "config_dir": str(tmp_path)}
    result, command, _lookup = run_module(codex_plugin, params, version="codex-cli 0.152.0\n")
    assert result["failed"] is True
    assert command.call_args.args[0] == VERSION_ARGS
    assert command.call_args.kwargs == {"environ_update": {"CODEX_HOME": str(tmp_path)}}
