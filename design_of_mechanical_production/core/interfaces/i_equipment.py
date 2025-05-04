#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Protocol


class IEquipment(Protocol):
    """
    Интерфейс для оборудования.
    """

    name: str
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
        Площадь оборудования.
        """
        return ...

    @property
    def power(self) -> Decimal:
        """
        Мощность оборудования.
        """
        return ...

    @property
    def dimensions(self) -> Dict[str, Decimal]:
        """
        Габариты оборудования.
        """
        return ...
