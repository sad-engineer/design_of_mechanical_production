#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Protocol


class IAreaCalculator(Protocol):
    """
    Интерфейс для калькуляторов площади.
    """

    def calculate_area(self, machines: Dict[str, 'IMachineInfo']) -> Decimal:
        """
        Рассчитывает площадь зоны.

        Args:
            machines: Словарь с информацией о станках

        Returns:
            Decimal: Рассчитанная площадь
        """
        ...
