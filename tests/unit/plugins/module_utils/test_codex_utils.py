"""Executable resolution and CLI response validation."""

from unittest.mock import Mock

import pytest

from ansible_collections.linuxhq.macos.plugins.module_utils import codex
from ansible_collections.linuxhq.macos.plugins.modules import codex_plugin


@pytest.mark.parametrize(
    "response,message",
    [
        ((1, "fallback detail", " stderr detail \n"), "stderr detail"),
        ((1, " fallback detail \n", ""), "fallback detail"),
        ((0, "not json", ""), "Unable to parse codex output"),
        ((0, "[]", ""), "Unexpected codex output"),
        ((0, '{"installed": null}', ""), "Unexpected codex output"),
        ((0, '{"installed": [1]}', ""), "Unexpected codex output"),
        ((0, "{}", ""), "Unexpected codex output"),
    ],
)
def test_invalid_cli_response(run_module, response, message):
    result, command, _lookup = run_module(codex_plugin, {"name": "editor", "marketplace": "example"}, [response])
    assert result["failed"] is True
    assert message in result["msg"]
    assert command.call_count == 1


def test_config_directory_is_passed_to_command(run_module, tmp_path):
    config = str(tmp_path / "config with spaces")
    result, command, _lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "example", "state": "absent", "config_dir": config},
        [{"installed": []}],
    )
    assert result["changed"] is False
    assert command.call_args.kwargs == {"environ_update": {"CODEX_HOME": config}}


def test_explicit_executable(run_module, tmp_path):
    executable = tmp_path / "codex tool"
    executable.touch(mode=0o755)
    result, command, lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "example", "state": "absent", "executable": str(executable)},
        [{"installed": []}],
    )
    assert result["changed"] is False
    assert command.call_args.args[0][0] == str(executable)
    lookup.assert_not_called()


@pytest.mark.parametrize("kind", ["missing", "directory", "nonexecutable"])
def test_invalid_explicit_executable(run_module, tmp_path, kind):
    path = tmp_path / "codex"
    if kind == "directory":
        path.mkdir()
    elif kind == "nonexecutable":
        path.touch(mode=0o644)

    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "example", "executable": str(path)}
    )
    assert result["failed"] is True
    assert "Unable to locate codex executable" in result["msg"]
    command.assert_not_called()


def test_missing_optional_explicit_executable(run_module, tmp_path):
    result, command, _lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "example", "executable": str(tmp_path / "missing")},
        check_mode=True,
    )
    assert result["changed"] is True
    command.assert_not_called()


def test_required_executable_lookup(run_module):
    result, command, lookup = run_module(codex_plugin, {"name": "editor", "marketplace": "example"}, executable=None)
    assert result["failed"] is True
    lookup.assert_called_once_with("codex", opt_dirs=["/usr/local/bin", "/opt/homebrew/bin"])
    command.assert_not_called()


def test_expand_executable_home(monkeypatch):
    module = Mock(params={"executable": "~/bin/codex"})
    monkeypatch.setattr(codex.os.path, "expanduser", lambda value: "/home/test/bin/codex")
    monkeypatch.setattr(codex.os.path, "isfile", lambda value: value == "/home/test/bin/codex")
    monkeypatch.setattr(codex.os, "access", lambda value, mode: value == "/home/test/bin/codex")
    assert codex.codex_bin(module) == "/home/test/bin/codex"
    module.fail_json.assert_not_called()


def test_result_conversion_is_recursive_and_does_not_mutate_input():
    original = {"pluginId": "editor@example", "nestedData": {"sourceType": "git"}}
    assert codex.codex_result(original) == {"plugin_id": "editor@example", "nested_data": {"source_type": "git"}}
    assert original == {"pluginId": "editor@example", "nestedData": {"sourceType": "git"}}
    assert codex.codex_result(None) is None
