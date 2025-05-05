from unittest.mock import patch, MagicMock


def test_mocked_creator():
    fake_tool = MagicMock()
    fake_tool.model = "DMG CTX beta 2000"

    with patch("machine_tools.MachineToolsContainer.creator") as mocked_creator:
        mocked_creator.return_value.by_name.return_value = fake_tool

        from design_of_mechanical_production.core.entities.machine_tool_source import DatabaseMachineToolSource
        result = DatabaseMachineToolSource.get_machine_tool("DMG CTX beta 2000")

        assert result.model == "DMG CTX beta 2000"