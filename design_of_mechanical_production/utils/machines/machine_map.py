#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from design_of_mechanical_production.utils.machines.machine_tool_operation_map import *


class MachineToolOperationMapFactory:
    """Фабрика для создания и управления картами операций."""

    def __init__(self):
        self.operation_getters = (
            ConventionalTurningMachineToolMap(),
            CNCTurningMachineToolMap(),

            ConventionalBoringMachineToolMap(),
            CNCBoringMachineToolMap(),

            ConventionalMultiPurposeMachineToolMap(),
            CNCMultiPurposeMachineToolMap(),

            ConventionalDrillingMachineToolMap(),
            CNCDrillingMachineToolMap(),

            ConventionalMillingMachineToolMap(),
            CNCMillingMachineToolMap(),

            ConventionalGrindingMachineToolMap(),
            CNCGrindingMachineToolMap(),

            ConventionalPlaningMachineToolMap(),
            CNCPlaningMachineToolMap(),

            ConventionalSlottingMachineToolMap(),
            CNCSlottingMachineToolMap(),

            ConventionalBroachingMachineToolMap(),
            CNCBroachingMachineToolMap(),

            ConventionalGearCuttingMachineToolMap(),
            CNCGearCuttingMachineToolMap(),

            ConventionalThreadCuttingMachineToolMap(),
            CNCThreadCuttingMachineToolMap(),
        )

    def get_map(self) -> dict:
        """
        Получение словаря с операциями и доступными именами станков. Если список станков пуст,
        то операция не будет добавлена в словарь.

        Returns:
            dict: Словарь {название операции: список станков}
        """
        _names_map = {}
        for operation_getter in self.operation_getters:
            if operation_getter.machine_tools:
                _names_map[operation_getter.operation_name] = operation_getter.machine_tools
        return _names_map


MACHINE_TOOL_OPERATION_MAP = MachineToolOperationMapFactory().get_map()


if __name__ == "__main__":
    for operation_name, machines in MACHINE_TOOL_OPERATION_MAP.items():
        print(f"{operation_name}: {len(machines)}")
