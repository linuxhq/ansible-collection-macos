"""Homebrew query selection, normalized results, and failures."""

import pytest

from ansible_collections.linuxhq.macos.plugins.modules import homebrew_cask_info, homebrew_info, homebrew_services_info


@pytest.mark.parametrize(
    "plugin,key,kind", [(homebrew_info, "formulae", "formula"), (homebrew_cask_info, "casks", "cask")]
)
@pytest.mark.parametrize("names", [None, ["one", "two"]])
@pytest.mark.parametrize("check_mode", [False, True])
def test_package_query(run_module, plugin, key, kind, names, check_mode):
    result, command, lookup = run_module(
        plugin, {"name": names, "path": "/custom/bin:/other/bin"}, [{key: []}], check_mode
    )
    assert result == {"changed": False, key: []}
    assert command.call_args.args[0] == [
        "/mock/bin/tool",
        "info",
        "--json=v2",
        f"--{kind}",
        *(names or ["--installed"]),
    ]
    lookup.assert_called_once_with("brew", opt_dirs=["/custom/bin", "/other/bin"])


def test_formula_normalization(run_module):
    formula = {
        "name": "wget",
        "desc": "Downloader",
        "installed": [{"version": "1.0"}, {"version": "2.0"}],
        "versions": {"stable": "2.0"},
        "tap": "homebrew/core",
        "pinned": True,
        "outdated": True,
        "deprecated": True,
    }
    result, _command, _lookup = run_module(homebrew_info, responses=[{"formulae": [formula, {"name": "empty"}]}])
    assert result["formulae"] == [
        {
            "name": "wget",
            "description": "Downloader",
            "installed": ["1.0", "2.0"],
            "version": "2.0",
            "tap": "homebrew/core",
            "pinned": True,
            "outdated": True,
            "deprecated": True,
        },
        {
            "name": "empty",
            "description": None,
            "installed": [],
            "version": None,
            "tap": None,
            "pinned": False,
            "outdated": False,
            "deprecated": False,
        },
    ]


def test_cask_normalization(run_module):
    result, _command, _lookup = run_module(
        homebrew_cask_info,
        responses=[
            {
                "casks": [
                    {
                        "token": "app",
                        "desc": "An app",
                        "installed": "1.0",
                        "version": "2.0",
                        "tap": "homebrew/cask",
                        "deprecated": True,
                        "outdated": True,
                    },
                    {},
                ]
            }
        ],
    )
    assert result["casks"] == [
        {
            "name": "app",
            "description": "An app",
            "installed": "1.0",
            "version": "2.0",
            "tap": "homebrew/cask",
            "deprecated": True,
            "outdated": True,
        },
        {
            "name": None,
            "description": None,
            "installed": None,
            "version": None,
            "tap": None,
            "deprecated": False,
            "outdated": False,
        },
    ]


@pytest.mark.parametrize("names", [None, ["redis"]])
def test_services_filter_missing_files(run_module, tmp_path, names):
    plist = tmp_path / "service.plist"
    plist.touch()
    service = {
        "name": "redis",
        "file": str(plist),
        "pid": 123,
        "exit_code": 0,
        "status": "started",
        "user": "tester",
        "loaded": True,
        "registered": True,
        "running": True,
    }
    result, command, _lookup = run_module(
        homebrew_services_info,
        {"name": names},
        [[service, {"name": "missing", "file": str(tmp_path / "missing")}, {"name": "uninstalled"}]],
        check_mode=True,
    )
    assert result == {"changed": False, "services": [service]}
    assert command.call_args.args[0] == ["/mock/bin/tool", "services", "info", "--json", *(names or ["--all"])]


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_cask_info, homebrew_services_info])
@pytest.mark.parametrize(
    "response,message",
    [((1, "", " brew error \n"), "brew error"), ((0, "not json", ""), "Unable to parse brew output")],
)
def test_command_failures(run_module, plugin, response, message):
    result, command, _lookup = run_module(plugin, responses=[response])
    assert result["failed"] is True
    assert message in result["msg"]
    assert command.call_count == 1


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_cask_info, homebrew_services_info])
def test_missing_brew(run_module, plugin):
    result, command, _lookup = run_module(plugin, executable=None)
    assert result == {"failed": True, "msg": "Unable to locate brew executable."}
    command.assert_not_called()
