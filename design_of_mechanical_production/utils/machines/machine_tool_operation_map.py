#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import List, Callable

from design_of_mechanical_production.utils.machines.finder import MachineFinderForOperations


class MachineToolOperationMap(ABC):
    """Базовый класс. Хранит условия соответствия имен станков для конкретного вида механической операции."""

    def __init__(self, find_function: str, name: str):
        self.machine_finder = MachineFinderForOperations()
        self._find_function: Callable = getattr(self.machine_finder, find_function)
        self._name: str = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.machine_finder.session:
            self.machine_finder.session_manager.close_session()

    @property
    def operation_name(self) -> str:
        """Название операции."""
        return self._name

    @operation_name.setter
    def operation_name(self, name: str) -> None:
        self._name = name

    @property
    @abstractmethod
    def machine_tools(self) -> List[str]:
        """Список имен станков."""
        pass


class TurningMachineToolMap(MachineToolOperationMap):
    """Класс для токарных операций."""

    def __init__(self, find_function: str, name: str = "Токарная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для токарных операций загружаем только станки первой группы
        machine_tools.extend(self._find_function(group=1))
        # в девятой группе сейчас только токарные станки, поэтому загружаем их
        machine_tools.extend(self._find_function(group=9))
        return machine_tools


class BoringMachineToolMap(MachineToolOperationMap):
    """Класс для расточных операций."""

    def __init__(self, find_function: str, name: str = "Расточная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для расточных операций загружаем только станки второй группы и подгрупп расточных станков
        machine_tools.extend(self._find_function(group=2, subgroups=[2, 3, 4, 6, 7, 9]))
        return machine_tools


class DrillingMachineToolMap(MachineToolOperationMap):
    """Класс для сверлильных операций."""

    def __init__(self, find_function: str, name: str = "Сверлильная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для сверлильных операций загружаем только станки второй группы и подгрупп сверлильных станков
        machine_tools.extend(self._find_function(group=2, subgroups=[1, 2, 3, 5, 8, 9]))
        return machine_tools


class GrindingMachineToolMap(MachineToolOperationMap):
    """Класс для шлифовальных операций."""

    def __init__(self, find_function: str, name: str = "Шлифовальная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для шлифовальных операций загружаем только станки третьей группы
        machine_tools.extend(self._find_function(group=3))
        return machine_tools


class GearCuttingMachineToolMap(MachineToolOperationMap):
    """Класс для зубообрабатывающих операций."""

    def __init__(self, find_function: str, name: str = "Зубообрабатывающая"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для зубообрабатывающих операций загружаем только станки пятой группы и подгрупп зубообрабатывающих станков
        machine_tools.extend(self._find_function(group=5, subgroups=[1, 2, 3, 4, 5, 7, 8, 9]))
        return machine_tools


class ThreadCuttingMachineToolMap(MachineToolOperationMap):
    """Класс для резьбообрабатывающих операций."""

    def __init__(self, find_function: str, name: str = "Резьбообрабатывающая"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для резьбообрабатывающих операций загружаем только станки пятой группы и подгрупп резьбообрабатывающих станков
        machine_tools.extend(self._find_function(group=5, subgroups=[0, 6, 8, 9]))
        return machine_tools


class MillingMachineToolMap(MachineToolOperationMap):
    """Класс для фрезерных операций."""

    def __init__(self, find_function: str, name: str = "Фрезерная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для фрезерных операций загружаем только станки шестой группы
        machine_tools.extend(self._find_function(group=6))
        return machine_tools


class PlaningMachineToolMap(MachineToolOperationMap):
    """Класс для строгальных операций."""

    def __init__(self, find_function: str, name: str = "Строгальная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для строгальных операций загружаем только станки седьмой группы и подгрупп строгальных станков
        machine_tools.extend(self._find_function(group=7, subgroups=[1, 2, 3, 9]))
        return machine_tools


class SlottingMachineToolMap(MachineToolOperationMap):
    """Класс для долбежных операций."""

    def __init__(self, find_function: str, name: str = "Долбежная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для долбежных операций загружаем только станки седьмой группы и подгрупп долбежных станков
        machine_tools.extend(self._find_function(group=7, subgroups=4))
        return machine_tools


class BroachingMachineToolMap(MachineToolOperationMap):
    """Класс для протяжных операций."""

    def __init__(self, find_function: str, name: str = "Протяжная"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для протяжных операций загружаем только станки седьмой группы и подгрупп протяжных станков
        machine_tools.extend(self._find_function(group=7, subgroups=[5, 7]))
        return machine_tools


class MultiPurposeMachineToolMap(MachineToolOperationMap):
    """Класс для многоцелевых операций."""

    def __init__(self, find_function: str, name: str = "Многоцелевая"):
        super().__init__(find_function, name)

    @property
    def machine_tools(self) -> List[str]:
        machine_tools = []
        # для многоцелевых операций загружаем все станки
        machine_tools.extend(self._find_function())
        return machine_tools


class ConventionalTurningMachineToolMap(TurningMachineToolMap):
    """Класс для токарных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Токарная")


class CNCTurningMachineToolMap(TurningMachineToolMap):
    """Класс для токарных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Токарная с ЧПУ")


class ConventionalBoringMachineToolMap(BoringMachineToolMap):
    """Класс для расточных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Расточная")


class CNCBoringMachineToolMap(BoringMachineToolMap):
    """Класс для расточных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Расточная с ЧПУ")


class ConventionalDrillingMachineToolMap(DrillingMachineToolMap):
    """Класс для сверлильных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Сверлильная")


class CNCDrillingMachineToolMap(DrillingMachineToolMap):
    """Класс для сверлильных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Сверлильная с ЧПУ")


class ConventionalMillingMachineToolMap(MillingMachineToolMap):
    """Класс для фрезерных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Фрезерная")


class CNCMillingMachineToolMap(MillingMachineToolMap):
    """Класс для фрезерных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Фрезерная с ЧПУ")


class ConventionalGrindingMachineToolMap(GrindingMachineToolMap):
    """Класс для шлифовальных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Шлифовальная")


class CNCGrindingMachineToolMap(GrindingMachineToolMap):
    """Класс для шлифовальных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Шлифовальная с ЧПУ")


class ConventionalGearCuttingMachineToolMap(GearCuttingMachineToolMap):
    """Класс для зубообрабатывающих операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Зубообрабатывающая")


class CNCGearCuttingMachineToolMap(GearCuttingMachineToolMap):
    """Класс для зубообрабатывающих операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Зубообрабатывающая с ЧПУ")


class ConventionalThreadCuttingMachineToolMap(ThreadCuttingMachineToolMap):
    """Класс для резьбообрабатывающих операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Резьбообрабатывающая")


class CNCThreadCuttingMachineToolMap(ThreadCuttingMachineToolMap):
    """Класс для резьбообрабатывающих операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Резьбообрабатывающая с ЧПУ")


class ConventionalPlaningMachineToolMap(PlaningMachineToolMap):
    """Класс для строгальных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Строгальная")


class CNCPlaningMachineToolMap(PlaningMachineToolMap):
    """Класс для строгальных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Строгальная с ЧПУ")


class ConventionalSlottingMachineToolMap(SlottingMachineToolMap):
    """Класс для долбежных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Расточная")


class CNCSlottingMachineToolMap(SlottingMachineToolMap):
    """Класс для долбежных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Расточная с ЧПУ")


class ConventionalBroachingMachineToolMap(BroachingMachineToolMap):
    """Класс для протяжных операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Протяжная")


class CNCBroachingMachineToolMap(BroachingMachineToolMap):
    """Класс для протяжных операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Протяжная с ЧПУ")


class ConventionalMultiPurposeMachineToolMap(MultiPurposeMachineToolMap):
    """Класс для многоцелевых операций без ЧПУ."""

    def __init__(self):
        super().__init__("get_no_cnc_names", "Многоцелевая")


class CNCMultiPurposeMachineToolMap(MultiPurposeMachineToolMap):
    """Класс для многоцелевых операций с ЧПУ."""

    def __init__(self):
        super().__init__("get_cnc_names", "Многоцелевая с ЧПУ")
