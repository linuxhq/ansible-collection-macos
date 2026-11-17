"""Homebrew query selection, unmodified results, unknown names, and failures."""

import os

import pytest

from ansible_collections.linuxhq.macos.plugins.modules import homebrew_cask_info, homebrew_info, homebrew_services_info

FORMULA = {
    "name": "wget",
    "full_name": "wget",
    "tap": "homebrew/core",
    "desc": "Internet file retriever",
    "versions": {"stable": "1.25.0", "head": "HEAD", "bottle": True},
    "installed": [{"version": "1.25.0", "installed_on_request": True, "runtime_dependencies": []}],
    "linked_keg": "1.25.0",
    "pinned": False,
    "outdated": False,
    "deprecated": False,
}

CASK = {
    "token": "iterm2",
    "full_token": "iterm2",
    "tap": "homebrew/cask",
    "name": ["iTerm2"],
    "desc": "Terminal emulator as alternative to Apple's Terminal app",
    "version": "3.7.6",
    "installed": "3.7.2",
    "outdated": True,
    "deprecated": False,
}

UNAVAILABLE = {
    "formula": 'Error: No available formula with the name "{name}".\n',
    "cask": "Error: Cask '{name}' is unavailable: No Cask with this name exists.\n",
    "service": 'Error: No available formula with the name "{name}".\n',
}


def service(name, file, registered=False):
    return {
        "name": name,
        "service_name": f"homebrew.mxcl.{name}",
        "running": False,
        "loaded": False,
        "schedulable": False,
        "pid": None,
        "exit_code": None,
        "user": None,
        "status": "none",
        "file": file,
        "registered": registered,
        "loaded_file": None,
    }


PACKAGES = [
    (homebrew_info, "formulae", "formula", FORMULA),
    (homebrew_cask_info, "casks", "cask", CASK),
]


@pytest.mark.parametrize("plugin,key,kind,_item", PACKAGES)
@pytest.mark.parametrize("names", [None, ["one", "two"]])
@pytest.mark.parametrize("check_mode", [False, True])
def test_package_query(run_module, plugin, key, kind, _item, names, check_mode):
    result, command, lookup = run_module(
        plugin, {"name": names, "path": "/custom/bin:/other/bin"}, [{key: []}], check_mode
    )
    assert result == {"changed": False, key: []}
    assert command.call_args.args[0] == [
        "/mock/bin/tool",
        "info",
        "--json=v2",
        f"--{kind}",
        *(["--", *names] if names else ["--installed"]),
    ]
    lookup.assert_called_once_with("brew", opt_dirs=["/custom/bin", "/other/bin"])


@pytest.mark.parametrize("plugin,key,_kind,item", PACKAGES)
def test_package_items_are_unmodified(run_module, plugin, key, _kind, item):
    result, _command, _lookup = run_module(plugin, responses=[{"formulae": [], "casks": [], key: [item]}])
    assert result == {"changed": False, key: [item]}


@pytest.mark.parametrize("plugin,key,kind,item", PACKAGES)
def test_package_unknown_names_are_omitted(run_module, plugin, key, kind, item):
    known = item.get("token", item["name"])
    unavailable = (1, "", UNAVAILABLE[kind].format(name="missing"))
    result, command, _lookup = run_module(
        plugin, {"name": [known, "missing"]}, [unavailable, {key: [item]}, unavailable]
    )
    assert result == {"changed": False, key: [item]}
    assert [call.args[0][4:] for call in command.call_args_list] == [
        ["--", known, "missing"],
        ["--", known],
        ["--", "missing"],
    ]


@pytest.mark.parametrize(
    "plugin,output",
    [(homebrew_info, {"formulae": []}), (homebrew_cask_info, {"casks": []}), (homebrew_services_info, [])],
)
def test_color_is_disabled(run_module, plugin, output):
    unavailable = (1, "", UNAVAILABLE["formula"].format(name="missing"))
    result, command, _lookup = run_module(plugin, {"name": ["one", "missing"]}, [unavailable, output, unavailable])
    assert result["changed"] is False
    environ_update = {"HOMEBREW_NO_COLOR": "1", "GITHUB_ACTIONS": ""}
    assert [call.kwargs for call in command.call_args_list] == [
        {"environ_update": environ_update, "expand_user_and_vars": False}
    ] * 3


@pytest.mark.parametrize(
    "plugin,output",
    [(homebrew_info, {"formulae": []}), (homebrew_cask_info, {"casks": []}), (homebrew_services_info, [])],
)
def test_github_actions_annotations_are_disabled(run_module, monkeypatch, plugin, output):
    monkeypatch.setenv("CI", "true")
    monkeypatch.setenv("GITHUB_ACTIONS", "true")

    def unavailable(args, environ_update, **_kwargs):
        # Homebrew prints errors as GitHub Actions annotations while GITHUB_ACTIONS is non-empty.
        prefix = "::error::" if {**os.environ, **environ_update}["GITHUB_ACTIONS"] else "Error: "
        return 1, "", f'{prefix}No available formula with the name "missing".\n'

    result, _command, _lookup = run_module(plugin, {"name": ["one", "missing"]}, [unavailable, output, unavailable])
    assert result["changed"] is False
    assert result.get("failed") is None


@pytest.mark.parametrize("plugin,key,kind,item", PACKAGES)
def test_package_option_names_are_not_options(run_module, plugin, key, kind, item):
    unavailable = (1, "", UNAVAILABLE[kind].format(name="--installed"))
    result, command, _lookup = run_module(plugin, {"name": ["--installed"]}, [unavailable, unavailable])
    assert result == {"changed": False, key: []}
    assert [call.args[0][3:] for call in command.call_args_list] == [[f"--{kind}", "--", "--installed"]] * 2


@pytest.mark.parametrize("plugin,key,kind,item", PACKAGES)
def test_package_duplicates_are_removed(run_module, plugin, key, kind, item):
    other = {**item, ("full_token" if kind == "cask" else "full_name"): "other"}
    known = item.get("token", item["name"])
    unavailable = (1, "", UNAVAILABLE[kind].format(name="missing"))
    batch, batch_command, _lookup = run_module(plugin, {"name": [known, known]}, [{key: [item, other, item]}])
    fallback, fallback_command, _lookup = run_module(
        plugin,
        {"name": [known, known, "missing"]},
        [unavailable, {key: [item]}, {key: [item]}, unavailable],
    )
    assert batch == {"changed": False, key: [item, other]}
    assert fallback == {"changed": False, key: [item]}
    assert batch_command.call_count == 1
    assert fallback_command.call_count == 4


def test_services_option_names_are_not_options(run_module):
    unavailable = (1, "", UNAVAILABLE["service"].format(name="--all"))
    result, command, _lookup = run_module(homebrew_services_info, {"name": ["--all"]}, [unavailable, unavailable])
    assert result == {"changed": False, "services": []}
    assert [call.args[0][1:] for call in command.call_args_list] == [["services", "info", "--json", "--", "--all"]] * 2


def test_services_duplicates_are_removed(run_module, tmp_path):
    plist = tmp_path / "service.plist"
    plist.touch()
    present = service("privoxy", str(plist))
    unavailable = (1, "", UNAVAILABLE["service"].format(name="missing"))
    batch, _command, _lookup = run_module(
        homebrew_services_info, {"name": ["privoxy", "privoxy"]}, [[present, present]]
    )
    fallback, command, _lookup = run_module(
        homebrew_services_info,
        {"name": ["privoxy", "privoxy", "missing"]},
        [unavailable, [present], [present], unavailable],
    )
    assert batch == fallback == {"changed": False, "services": [present]}
    assert command.call_count == 4


@pytest.mark.parametrize(
    "stderr",
    [
        "Error: Cask 'homebrew/cask/missing' is unavailable.\nThis command requires the tap homebrew/cask.\n",
        'Error: No available formula or cask with the name "missing".\n',
        "Error: Cask 'missing' is unavailable: '/opt/homebrew/Library/Taps/u/homebrew-t/Casks/x.rb' does not exist.\n",
        "Error: Cask 'it's' is unavailable: No Cask with this name exists.\n",
        "Error: Cask 'foo bar' is unavailable: Invalid cask name.\n",
        "Error: Cask 'a/b/c/d' is unavailable: Invalid cask name.\n",
        "Error: Cask '' is unavailable: Invalid cask name.\n",
    ],
)
def test_unavailable_variants_are_omitted(run_module, stderr):
    result, command, _lookup = run_module(homebrew_cask_info, {"name": ["missing"]}, [(1, "", stderr)] * 2)
    assert result == {"changed": False, "casks": []}
    assert command.call_count == 2


@pytest.mark.parametrize("reason", ["is not readable", "is not a file"])
def test_unloadable_cask_path_fails(run_module, reason):
    stderr = (
        f"Error: Cask 'one' is unavailable: '/opt/homebrew/Library/Taps/user/homebrew-tap/Casks/one.rb' {reason}.\n"
    )
    result, command, _lookup = run_module(homebrew_cask_info, {"name": ["one"]}, [(1, "", stderr)])
    assert result["failed"] is True
    assert reason in result["msg"]
    assert command.call_count == 1


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_services_info])
def test_unloadable_formula_class_fails(run_module, plugin):
    stderr = (
        'Error: No available formula with the name "user/tap/broken".\n'
        "In formula file: /opt/homebrew/Library/Taps/user/homebrew-tap/Formula/broken.rb\n"
        "Expected to find class Broken, but only found: Other.\n"
    )
    result, command, _lookup = run_module(plugin, {"name": ["user/tap/broken"]}, [(1, "", stderr)])
    assert result["failed"] is True
    assert "Expected to find class Broken" in result["msg"]
    assert command.call_count == 1


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_services_info])
def test_unknown_formula_with_suggestion_is_omitted(run_module, plugin):
    stderr = 'Error: No available formula with the name "wgett". Did you mean wget?\n'
    result, command, _lookup = run_module(plugin, {"name": ["wgett"]}, [(1, "", stderr)] * 2)
    assert result["changed"] is False
    assert command.call_count == 2


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_cask_info, homebrew_services_info])
def test_other_failure_during_name_retry_fails(run_module, plugin):
    stderr = "Error: Cask 'one' is unavailable: Failed to download https://example.test.\n"
    responses = [(1, "", UNAVAILABLE["formula"].format(name="two")), (1, "", stderr)]
    result, command, _lookup = run_module(plugin, {"name": ["one", "two"]}, responses)
    assert result["failed"] is True
    assert "Failed to download" in result["msg"]
    assert command.call_count == 2


@pytest.mark.parametrize("names", [None, ["redis"]])
def test_services_selection(run_module, tmp_path, names):
    plist = tmp_path / "service.plist"
    plist.touch()
    present = service("redis", str(plist))
    root = service("root", str(tmp_path / "LaunchAgents" / "homebrew.mxcl.root.plist"), registered=True)
    result, command, _lookup = run_module(
        homebrew_services_info,
        {"name": names},
        [[present, root, service("uninstalled", str(tmp_path / "missing"))]],
        check_mode=True,
    )
    assert result == {"changed": False, "services": [present, root]}
    assert command.call_args.args[0] == [
        "/mock/bin/tool",
        "services",
        "info",
        "--json",
        *(["--", *names] if names else ["--all"]),
    ]


def test_services_all_without_services(run_module):
    result, _command, _lookup = run_module(homebrew_services_info, responses=[(0, "", "")])
    assert result == {"changed": False, "services": []}


def test_services_unknown_names_are_omitted(run_module, tmp_path):
    plist = tmp_path / "service.plist"
    plist.touch()
    present = service("redis", str(plist))
    unavailable = (1, "", UNAVAILABLE["service"].format(name="missing"))
    result, command, _lookup = run_module(
        homebrew_services_info, {"name": ["missing", "redis"]}, [unavailable, unavailable, [present]]
    )
    assert result == {"changed": False, "services": [present]}
    assert command.call_count == 3


@pytest.mark.parametrize(
    "plugin,names,operation",
    [
        (homebrew_info, None, "gather Homebrew formula information for installed formulae"),
        (homebrew_info, ["privoxy", "rclone"], "gather Homebrew formula information for privoxy, rclone"),
        (homebrew_cask_info, None, "gather Homebrew cask information for installed casks"),
        (homebrew_cask_info, ["iterm2"], "gather Homebrew cask information for iterm2"),
        (homebrew_services_info, None, "gather Homebrew service information for all services"),
        (homebrew_services_info, ["privoxy"], "gather Homebrew service information for privoxy"),
    ],
)
@pytest.mark.parametrize(
    "response,message",
    [
        ((1, "", " brew error \n"), "Unable to {operation}: brew error"),
        ((1, " stdout detail \n", ""), "Unable to {operation}: stdout detail"),
    ],
)
def test_command_failures(run_module, plugin, names, operation, response, message):
    result, command, _lookup = run_module(plugin, {"name": names}, [response])
    assert result["failed"] is True
    assert result["msg"].startswith(message.format(operation=operation))
    assert command.call_count == 1


@pytest.mark.parametrize("plugin", [homebrew_info, homebrew_cask_info, homebrew_services_info])
def test_missing_brew(run_module, plugin):
    result, command, _lookup = run_module(plugin, executable=None)
    assert result == {"failed": True, "msg": "Unable to locate brew executable."}
    command.assert_not_called()


@pytest.mark.parametrize("plugin,key,kind,_item", PACKAGES)
@pytest.mark.parametrize("name", ["$HOMEBREW_PROBE", "~"])
def test_package_names_are_not_expanded(run_module, monkeypatch, plugin, key, kind, _item, name):
    monkeypatch.setenv("HOMEBREW_PROBE", "wget")
    received = []

    def query(args, **_kwargs):
        received.append(args)
        return {key: []}

    result, _command, _lookup = run_module(plugin, {"name": [name]}, [query])
    assert result == {"changed": False, key: []}
    assert received == [["/mock/bin/tool", "info", "--json=v2", f"--{kind}", "--", name]]


def test_service_names_are_not_expanded(run_module, monkeypatch):
    monkeypatch.setenv("HOMEBREW_PROBE", "wget")
    received = []

    def query(args, **_kwargs):
        received.append(args)
        return []

    result, _command, _lookup = run_module(homebrew_services_info, {"name": ["$HOMEBREW_PROBE"]}, [query])
    assert result == {"changed": False, "services": []}
    assert received == [["/mock/bin/tool", "services", "info", "--json", "--", "$HOMEBREW_PROBE"]]
