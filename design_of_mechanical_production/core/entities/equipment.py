#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Optional

from design_of_mechanical_production.core.interfaces import IEquipment


@dataclass
class Equipment(IEquipment):
    """
    Класс, представляющий оборудование в цехе.
    """

    name: Optional[str]
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

    @property
    def power(self) -> Decimal:
        """
        Возвращает потребляемую мощность оборудования.

        Returns:
            Мощность в кВт
        """
        return self.power_consumption

    @property
    def dimensions(self) -> Dict[str, Decimal]:
        """
        Возвращает габаритные размеры оборудования.

        Returns:
            Словарь с размерами (длина, ширина, высота)
        """
        return {'length': self.length, 'width': self.width, 'height': self.height}
