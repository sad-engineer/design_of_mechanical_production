#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Protocol, Union

from design_of_mechanical_production.core.interfaces import IAreaCalculator, IMachineInfo


class IWorkshopZone(Protocol):
    """
    Интерфейс для зоны цеха.
    """

    name: str
    machines: Dict[str, 'IMachineInfo']

    def calculate_area(self) -> Decimal:
        """
        Рассчитывает площадь зоны.
        """
        ...

    def add_machine(self, name: str, machine: 'IMachineInfo') -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        ...

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Расчетное количество станков.
        """
        return ...

    @property
    def accepted_machines_count(self) -> int:
        """
        Принятое количество станков.
        """
        return ...

    @property
    def area(self) -> Decimal:
        """
        Площадь зоны.
        """
        return ...


class ISpecificWorkshopZone(Protocol):
    """
        Класс, представляющий вспомогательную зону цеха.
        Площадь определяется по удельной площади в пересчете на количество элементов.
        """
    name: str                                           # Название зоны
    specific_area: Decimal                              # удельная площадь зоны в м²
    unit_of_calculation: Union[int, Decimal, float]   # количество элементов в зоне для расчета площади
    _area_calculator: 'IAreaCalculator'                 # Калькулятор площади

    @property
    def area(self) -> Decimal:
        """
        Площадь зоны.
        """
        return ...
