"""Executable resolution and CLI failure reporting."""

from unittest.mock import Mock

import pytest

from ansible_collections.linuxhq.macos.plugins.module_utils import codex
from ansible_collections.linuxhq.macos.plugins.modules import codex_plugin


@pytest.mark.parametrize(
    "response,message",
    [
        ((1, "fallback detail", " stderr detail \n"), "stderr detail"),
        ((1, " fallback detail \n", ""), "fallback detail"),
    ],
)
def test_cli_failure(run_module, response, message):
    result, command, _lookup = run_module(codex_plugin, {"name": "editor", "marketplace": "example"}, [response])
    assert result["failed"] is True
    assert message in result["msg"]
    assert command.call_count == 2


@pytest.mark.parametrize("changed", [False, True])
def test_cli_failure_reports_changed(monkeypatch, changed):
    monkeypatch.setattr(codex, "codex_run", lambda _module, _args: (1, "", "Error: boom\n"))
    module = Mock()
    module.fail_json.side_effect = SystemExit
    with pytest.raises(SystemExit):
        codex.codex_list(module, ["plugin", "list", "--json"], "installed", "list plugins", changed=changed)

    module.fail_json.assert_called_once_with(changed=changed, msg="Unable to list plugins: Error: boom")


def test_config_directory_is_passed_to_command(run_module, tmp_path):
    config = tmp_path / "config with spaces"
    config.mkdir()
    result, command, _lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "example", "state": "absent", "config_dir": str(config)},
        [{"installed": []}],
    )
    assert result["changed"] is False
    assert command.call_args.kwargs == {"environ_update": {"CODEX_HOME": str(config)}, "expand_user_and_vars": False}


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


def test_missing_explicit_executable(run_module, tmp_path):
    path = tmp_path / "codex"
    result, command, _lookup = run_module(
        codex_plugin, {"name": "editor", "marketplace": "example", "executable": str(path)}
    )
    assert result == {"failed": True, "msg": f"Unable to locate codex executable: {path}"}
    command.assert_not_called()


@pytest.mark.parametrize("kind", ["directory", "nonexecutable"])
def test_existing_explicit_executable_is_run(run_module, tmp_path, kind):
    path = tmp_path / "codex"
    if kind == "directory":
        path.mkdir()
    else:
        path.touch(mode=0o644)

    result, command, _lookup = run_module(
        codex_plugin,
        {"name": "editor", "marketplace": "example", "state": "absent", "executable": str(path)},
        [{"installed": []}],
    )
    assert result["changed"] is False
    assert command.call_args.args[0][0] == str(path)


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


def test_result_conversion_is_recursive_and_does_not_mutate_input():
    original = {"pluginId": "editor@example", "nestedData": {"sourceType": "git"}}
    assert codex.codex_result(original) == {"plugin_id": "editor@example", "nested_data": {"source_type": "git"}}
    assert original == {"pluginId": "editor@example", "nestedData": {"sourceType": "git"}}
    assert codex.codex_result(None) is None


@pytest.mark.parametrize(
    "config_dir,environment,expected",
    [
        ("{home}/custom", "/env/codex", "{home}/custom"),
        (None, "/env/codex", "/env/codex"),
        (None, "", "{home}/.codex"),
        (None, None, "{home}/.codex"),
    ],
)
def test_codex_home_resolution(monkeypatch, tmp_path, config_dir, environment, expected):
    monkeypatch.setenv("HOME", str(tmp_path))
    if environment is None:
        monkeypatch.delenv("CODEX_HOME", raising=False)
    else:
        monkeypatch.setenv("CODEX_HOME", environment)

    module = Mock(params={"config_dir": config_dir and config_dir.format(home=tmp_path)})
    assert codex.codex_home(module) == expected.format(home=tmp_path)
