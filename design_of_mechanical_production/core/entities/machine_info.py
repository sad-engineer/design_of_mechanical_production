#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import ceil
from typing import Union

from design_of_mechanical_production.core.interfaces import IEquipment, IMachineInfo


@dataclass
class MachineInfo(IMachineInfo):
    """
    Класс для хранения информации о станке в зоне.
    """

    model: Union[IEquipment, str]  # Название станка
    calculated_count: Decimal  # Расчетное количество станков

    def __post_init__(self) -> None:
        """
        Проверяет корректность данных после создания объекта.
        """
        if self.calculated_count < 0:
            raise ValueError("Количество станков не может быть отрицательным")

    @property
    def accepted_count(self) -> int:
        """
        Возвращает принятое количество станков (округленное вверх).
        """
        return ceil(self.calculated_count)
