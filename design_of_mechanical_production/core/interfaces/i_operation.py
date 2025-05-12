#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Optional, Protocol

from design_of_mechanical_production.core.interfaces import IEquipment


class IOperation(Protocol):
    """
    Интерфейс для операции.
    """

    number: str
    name: str
    time: Decimal
    equipment: 'IEquipment'
    calculated_equipment_count: Decimal  # Расчетное количество оборудования
    fund_of_working: Decimal  # Действительный фонд времени работы одного станка, ч
    compliance_coefficient: Decimal  # Коэффициент выполнения норм
    progressivity_coefficient: Decimal  # Коэффициент прогрессивности технологии

    @property
    def accepted_equipment_count(self) -> int:
        """
        Принятое количество оборудования.
        """
        return ...

    @property
    def load_factor(self) -> Decimal:
        """
        Коэффициент загрузки оборудования.
        """
        return ...

    @property
    def percentage(self) -> Optional[Decimal]:
        """
        Доля от общей трудоемкости.
        """
        return ...

    def accept_count(self, count: Optional[Decimal]) -> None:
        """
        Принимает количество оборудования.

        Args:
            count: Количество оборудования
        """
        ...

    def calculate_load_factor(self) -> None:
        """
        Рассчитывает коэффициент загрузки оборудования.
        """
        ...

    def calculate_percentage(self, total_time: Decimal) -> None:
        """
        Рассчитывает долю от общей трудоемкости.

        Args:
            total_time: Общее время на выполнение всех операций
        """
        ...
