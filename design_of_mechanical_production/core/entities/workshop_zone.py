#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Union

from design_of_mechanical_production.core.entities import AreaCalculator, SpecificAreaCalculator
from design_of_mechanical_production.core.interfaces import (
    IAreaCalculator,
    IMachineInfo,
    IWorkshopZone,
)
from design_of_mechanical_production.settings import get_setting


class BaseWorkshopZone(ABC):
    """
    Абстрактный базовый класс для всех типов зон цеха.
    """

    name: str  # Название зоны

    @property
    @abstractmethod
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        pass


@dataclass
class WorkshopZone(IWorkshopZone, BaseWorkshopZone):
    """
    Класс, представляющий зону цеха.
    """

    name: str
    machines: Dict[str, IMachineInfo] = field(default_factory=dict)
    _area_calculator: IAreaCalculator = None

    def __post_init__(self) -> None:
        """
        Инициализирует калькулятор площади после создания объекта.
        """
        if self._area_calculator is None:
            self._area_calculator = AreaCalculator(Decimal(get_setting("passage_area")))

    def calculate_area(self) -> Decimal:
        """
        Рассчитывает площадь зоны.
        """
        return self._area_calculator.calculate_area(self.machines)

    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        self.machines[name] = machine

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков в зоне.
        """
        return sum(machine.calculated_count for machine in self.machines.values())

    @property
    def accepted_machines_count(self) -> int:
        """
        Возвращает количество станков в зоне.
        """
        return sum(machine.accepted_count for machine in self.machines.values())

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        return self._area_calculator.calculate_area(self.machines)


@dataclass
class SpecificWorkshopZone(BaseWorkshopZone):
    """
    Класс, представляющий вспомогательную зону цеха.
    Площадь определяется по удельной площади в пересчете на количество элементов.
    """

    name: str  # Название зоны
    specific_area: Decimal  # удельная площадь зоны в м²
    total_equipment_count: Union[int, Decimal, float] = 0  # количество элементов в зоне для расчета площади
    _area_calculator: IAreaCalculator = None  # Калькулятор площади

    def __post_init__(self) -> None:
        """
        Инициализирует калькулятор площади после создания объекта.
        """
        if self._area_calculator is None:
            self._area_calculator = SpecificAreaCalculator(self.specific_area, self.total_equipment_count)

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        return self._area_calculator.calculate_area({})

    @property
    def total_calculated_equipment_count(self) -> Decimal:
        """
        Возвращает расчетное количество оборудования в зоне.
        """
        return Decimal(str(self.total_equipment_count))

    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        raise NotImplementedError("SpecificWorkshopZone не поддерживает добавление станков")
