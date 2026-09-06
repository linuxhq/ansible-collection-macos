"""Parse launchctl output without a running launchd service."""

import pytest

from ansible_collections.linuxhq.macos.plugins.modules import launchd_info


@pytest.mark.parametrize("check_mode", [False, True])
def test_services(run_module, check_mode):
    output = "PID\tStatus\tLabel\n123\t0\trunning\n-\t-9\tstopped\n\n\t\tempty\n"
    result, command, lookup = run_module(launchd_info, responses=[(0, output, "")], check_mode=check_mode)
    assert result == {
        "changed": False,
        "services": [
            {"label": "running", "pid": 123, "last_exit_status": 0, "running": True},
            {"label": "stopped", "pid": None, "last_exit_status": -9, "running": False},
            {"label": "empty", "pid": None, "last_exit_status": None, "running": False},
        ],
    }
    command.assert_called_once_with(["/mock/bin/tool", "list"])
    lookup.assert_called_once_with("launchctl", opt_dirs=["/bin"])


@pytest.mark.parametrize("names,expected", [(["one"], ["one"]), (["missing"], []), ([], ["one", "two"])])
def test_filter(run_module, names, expected):
    result, _command, _lookup = run_module(
        launchd_info, {"name": names}, [(0, "PID\tStatus\tLabel\n-\t0\tone\n-\t0\ttwo\n", "")]
    )
    assert [service["label"] for service in result["services"]] == expected


@pytest.mark.parametrize(
    "output,message",
    [
        ("", "header"),
        ("PID Status Label\n", "header"),
        ("PID\tStatus\tLabel\ninvalid\n", "line"),
        ("PID\tStatus\tLabel\n1\t0\tname\textra\n", "line"),
    ],
)
def test_malformed_output(run_module, output, message):
    result, _command, _lookup = run_module(launchd_info, responses=[(0, output, "")])
    assert result["failed"] is True
    assert message in result["msg"]


def test_empty_list(run_module):
    result, _command, _lookup = run_module(launchd_info, responses=[(0, "PID\tStatus\tLabel\n", "")])
    assert result == {"changed": False, "services": []}


def test_command_failure(run_module):
    result, _command, _lookup = run_module(launchd_info, responses=[(1, "", " permission denied \n")])
    assert result == {"failed": True, "msg": "Unable to gather launchd information: permission denied"}


def test_missing_launchctl(run_module):
    result, command, _lookup = run_module(launchd_info, executable=None)
    assert result == {"failed": True, "msg": "Unable to locate launchctl executable."}
    command.assert_not_called()
