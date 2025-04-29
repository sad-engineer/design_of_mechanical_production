#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Union
from decimal import Decimal

from design_of_mechanical_production.entities.machine_info import MachineInfo
from design_of_mechanical_production.entities.types import AreaCalculatorType
from design_of_mechanical_production.entities.area_calculator import AreaCalculator, SpecificAreaCalculator
from design_of_mechanical_production.settings import get_setting


class BaseWorkshopZone(ABC):
    """
    Абстрактный базовый класс для всех типов зон цеха.
    """
    name: str                                  # Название зоны

    @property
    @abstractmethod
    def area(self) -> Decimal:
        pass

    @property
    @abstractmethod
    def total_equipment_count(self) -> int:
        pass

    @property
    @abstractmethod
    def total_calculated_equipment_count(self) -> Decimal:
        pass


@dataclass
class WorkshopZone(BaseWorkshopZone):
    """
    Класс, представляющий основную зону цеха.
    """
    name: str                                  # Название зоны
    machines: Dict[str, MachineInfo]           # Словарь станок/информация о количестве
    _area_calculator: AreaCalculatorType = None   # Калькулятор площади

    def __post_init__(self):
        if self._area_calculator is None:
            self._area_calculator = AreaCalculator(Decimal(str(get_setting('passage_area'))))

    @property
    def area(self) -> Decimal:
        return self._area_calculator.calculate_area(self.machines)

    @property
    def total_equipment_count(self) -> int:
        """
        Общее количество станков в зоне.
        """
        return sum(machine.accepted_count for machine in self.machines.values())
    
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
    name: str                                               # Название зоны
    specific_area: Decimal                                  # удельная площадь зоны в м²
    total_equipment_count: Union[int, Decimal, float] = 0   # количество элементов в зоне для расчета площади
    _area_calculator: AreaCalculatorType = None                # Калькулятор площади

    def __post_init__(self):
        if self._area_calculator is None:
            self._area_calculator = SpecificAreaCalculator(
                self.specific_area,
                self.total_equipment_count
            )

    @property
    def area(self) -> Decimal:
        return self._area_calculator.calculate_area({})

    @property
    def total_calculated_equipment_count(self) -> Decimal:
        return Decimal(str(self.total_equipment_count))
