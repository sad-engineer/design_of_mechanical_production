#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Equipment:
    """
    Класс, представляющий оборудование в цехе.
    """
    model: str
    length: Decimal
    width: Decimal
    height: Decimal
    automation: str
    weight: Decimal
    power_consumption: Decimal

    @property
    def area(self) -> Decimal:
        """
        Рассчитывает площадь, занимаемую оборудованием.
        
        Returns:
            Площадь в квадратных метрах
        """
        return self.length * self.width
