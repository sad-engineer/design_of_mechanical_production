#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Union

from design_of_mechanical_production.core.entities.area_calculator import AreaCalculator, SpecificAreaCalculator
from design_of_mechanical_production.core.entities.types import AreaCalculatorType, IAreaCalculator, IMachineInfo, IWorkshopZone


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

    @property
    @abstractmethod
    def total_equipment_count(self) -> int:
        """
        Возвращает общее количество оборудования в зоне.
        """
        pass

    @property
    @abstractmethod
    def total_calculated_equipment_count(self) -> Decimal:
        """
        Возвращает расчетное количество оборудования в зоне.
        """
        pass

    @abstractmethod
    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        pass


@dataclass
class WorkshopZone(IWorkshopZone, BaseWorkshopZone):
    """
    Класс, представляющий зону цеха.
    """

    name: str
    machines: Dict[str, IMachineInfo] = field(default_factory=dict)
    area: Decimal = Decimal('0')
    total_equipment_count: int = 0
    _area_calculator: IAreaCalculator = None

    def __post_init__(self) -> None:
        """
        Инициализирует калькулятор площади после создания объекта.
        """
        if self._area_calculator is None:
            if self.name == "Основная зона":
                self._area_calculator = AreaCalculator(Decimal('2.5'))
            else:
                self._area_calculator = SpecificAreaCalculator(Decimal('4.5'), self.total_equipment_count)

    def calculate_area(self) -> Decimal:
        """
        Рассчитывает площадь зоны.
        """
        self.area = self._area_calculator.calculate_area(self.machines)
        return self.area

    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        self.machines[name] = machine
        self.total_equipment_count += machine.accepted_count

    @property
    def total_calculated_equipment_count(self) -> Decimal:
        """
        Общее расчетное количество станков в зоне.
        """
        return sum(machine.calculated_count for machine in self.machines.values())


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
