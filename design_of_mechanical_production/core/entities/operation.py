#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from design_of_mechanical_production.core.interfaces import IEquipment, IOperation


@dataclass
class Operation(IOperation):
    """
    Класс, представляющий операцию технологического процесса.
    """

    number: str
    name: str
    time: Decimal
    equipment: IEquipment
    calculated_equipment_count: Decimal = Decimal('0')  # Расчетное количество оборудования
    _accepted_equipment_count: int = 0  # Принятое количество станков (округленное вверх)
    _load_factor: Decimal = Decimal('0')  # Коэффициент загрузки станков
    _percentage: Optional[Decimal] = None  # Процентное соотношение операции

    def __post_init__(self) -> None:
        """
        Инициализирует объект после создания.
        """
        if self.time <= 0:
            raise ValueError("Время операции должно быть положительным")

    @property
    def accepted_equipment_count(self) -> int:
        """Возвращает принятое количество станков."""
        return self._accepted_equipment_count

    @property
    def load_factor(self) -> Decimal:
        """Возвращает коэффициент загрузки станков."""
        self.calculate_load_factor()
        return self._load_factor

    @property
    def percentage(self) -> Optional[Decimal]:
        """Возвращает процентное соотношение операции."""
        return self._percentage

    def accept_count(self, count: Optional[Decimal]) -> None:
        """ """
        if count < 0:
            raise ValueError("Принятое количество оборудования не может быть отрицательным")

        if count < self.calculated_equipment_count:
            raise ValueError("Принятое количество оборудования не может быть меньше расчетного")

        self._accepted_equipment_count = int(count)
        self.calculate_load_factor()

    def calculate_load_factor(self) -> None:
        """
        Рассчитывает коэффициент загрузки станков по формуле:
        К_З = С_Р / С_ПР
        где:
        С_Р - расчетное количество станков
        С_ПР - принятое количество станков
        """
        if self._accepted_equipment_count > 0:
            self._load_factor = self.calculated_equipment_count / Decimal(self._accepted_equipment_count)
        else:
            self._load_factor = Decimal('0')

    def calculate_percentage(self, total_time: Decimal) -> None:
        """
        Рассчитывает процентное соотношение операции.

        Args:
            total_time: Общее время технологического процесса
        """
        if total_time > 0:
            self._percentage = (self.time / total_time) * Decimal('100')
        else:
            raise ValueError("Общее время не может быть отрицательным или нулевым")
