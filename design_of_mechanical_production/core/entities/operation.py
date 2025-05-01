#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import ceil
from typing import Optional

from design_of_mechanical_production.core.entities.types import IEquipment, IOperation


@dataclass
class Operation(IOperation):
    """
    Класс, представляющий операцию технологического процесса.
    """

    number: int
    name: str
    time: Decimal
    equipment: IEquipment
    calculated_machines_count: Decimal = Decimal('0')  # Расчетное количество станков
    accepted_machines_count: int = 0  # Принятое количество станков (округленное вверх)
    load_factor: Decimal = Decimal('0')  # Коэффициент загрузки станков
    percentage: Optional[Decimal] = None

    def accept_machines_count(self) -> None:
        """
        Округляет расчетное количество станков вверх до целого числа
        и пересчитывает коэффициент загрузки.
        """
        self.accepted_machines_count = ceil(self.calculated_machines_count)
        self.calculate_load_factor()

    def calculate_load_factor(self) -> None:
        """
        Рассчитывает коэффициент загрузки станков по формуле:
        К_З = С_Р / С_ПР
        где:
        С_Р - расчетное количество станков
        С_ПР - принятое количество станков
        """
        if self.accepted_machines_count > 0:
            self.load_factor = self.calculated_machines_count / Decimal(self.accepted_machines_count)
        else:
            self.load_factor = Decimal('0')

    def calculate_percentage(self, total_time: Decimal) -> None:
        """
        Рассчитывает процентное соотношение операции.

        Args:
            total_time: Общее время процесса
        """
        self.percentage = (self.time / total_time) * Decimal('100')
