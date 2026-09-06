"""Run real Ansible argument validation while isolating external commands."""

import json
from unittest.mock import Mock

import pytest

from ansible.module_utils import basic


class ModuleResult(Exception):
    def __init__(self, result):
        self.result = result
        super().__init__(result.get("msg", "module exited"))


@pytest.fixture
def run_module(monkeypatch):
    def run(plugin, params=None, responses=(), check_mode=False, executable="/mock/bin/tool"):
        arguments = dict(params or {})
        arguments["_ansible_check_mode"] = check_mode
        monkeypatch.setattr(basic, "_load_params", lambda: arguments)

        def finish(self, **result):
            raise ModuleResult(result)

        def fail(self, **result):
            result["failed"] = True
            raise ModuleResult(result)

        command = Mock(
            side_effect=[(0, json.dumps(value), "") if not isinstance(value, tuple) else value for value in responses]
        )
        lookup = Mock(return_value=executable)
        monkeypatch.setattr(basic.AnsibleModule, "exit_json", finish)
        monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail)
        monkeypatch.setattr(basic.AnsibleModule, "run_command", command)
        monkeypatch.setattr(basic.AnsibleModule, "get_bin_path", lookup)
        with pytest.raises(ModuleResult) as raised:
            plugin.main()

        return raised.value.result, command, lookup

    return run
