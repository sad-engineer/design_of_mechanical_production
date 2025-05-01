#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Dict, Protocol

from design_of_mechanical_production.core.entities.machine_info import MachineInfo


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
