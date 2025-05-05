from unittest.mock import patch, MagicMock


def test_mocked_creator(monkeypatch):
    from design_of_mechanical_production.core.entities import machine_tool_source

    fake_tool = MagicMock()
    fake_tool.model = "DMG CTX beta 2000"

    class FakeCreator:
        def by_name(self, name):
            return fake_tool

    class FakeContainer:
        def creator(self):
            return FakeCreator()

    monkeypatch.setattr(machine_tool_source, "Container", lambda: FakeContainer())

    result = machine_tool_source.DatabaseMachineToolSource.get_machine_tool("DMG CTX beta 2000")
    assert result.model == "DMG CTX beta 2000"