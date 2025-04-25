#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Dict, Union
from decimal import Decimal
from math import ceil

from design_of_mechanical_production.domain.entities.equipment import Equipment
from design_of_mechanical_production.settings import get_setting


@dataclass
class MachineInfo:
    """
    Класс для хранения информации о станке в зоне.
    """
    model: Union[Equipment, str]  # Название станка
    calculated_count: Decimal  # Расчетное количество станков
    accepted_count: int  # Принятое количество станков (округленное вверх)
    
    def __init__(self, model: Equipment, calculated_count: Decimal):
        self.model = model
        self.calculated_count = calculated_count
        self.accepted_count = ceil(calculated_count)


@dataclass
class WorkshopZone:
    """
    Класс, представляющий зону цеха.
    """
    name: str  # Название зоны
    machines: Dict[str, MachineInfo]  # Словарь станок/информация о количестве
    
    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков в зоне.
        """
        return sum(machine.accepted_count for machine in self.machines.values())
    
    @property
    def total_calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков в зоне.
        """
        return sum(machine.calculated_count for machine in self.machines.values())

    @property
    def area(self) -> Decimal:
        """
        Общая площадь зоны с учетом проходов.
        """
        area = Decimal('0')
        passage_area = Decimal(str(get_setting('passage_area')))
        for name, machine in self.machines.items():
            length = machine.model.length
            width = machine.model.width
            area += (length * width + passage_area) * machine.accepted_count
        return area


@dataclass
class SpecificWorkshopZone:
    """
    Класс, представляющий вспомогательную зону цеха.
    Площадь определяется по удельной площади в пересчете на количество элементов.
    """
    name: str                                               # Название зоны
    specific_area: Decimal                                  # удельная площадь зоны в м²
    total_equipment_count: Union[int, Decimal, float] = 0   # количество элементов в зоне для расчета площади

    @property
    def area(self) -> Decimal:
        """
        Площадь в пересчете на количество станков.
        """
        return self.specific_area * self.total_equipment_count
