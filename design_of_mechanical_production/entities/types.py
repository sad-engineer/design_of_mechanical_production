#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Union, TypeVar, Protocol
from decimal import Decimal

from design_of_mechanical_production.entities.machine_info import MachineInfo


class IAreaCalculator(Protocol):
    """
    Интерфейс для калькуляторов площади.
    """
    def calculate_area(self, machines: Dict[str, MachineInfo]) -> Decimal:
        """
        Рассчитывает площадь зоны.
        
        Args:
            machines: Словарь с информацией о станках
            
        Returns:
            Decimal: Рассчитанная площадь
        """
        ...


# Типы для аннотаций
T = TypeVar('T')
AreaCalculatorType = Union['AreaCalculator', 'SpecificAreaCalculator']
WorkshopZoneType = Union['WorkshopZone', 'SpecificWorkshopZone']
