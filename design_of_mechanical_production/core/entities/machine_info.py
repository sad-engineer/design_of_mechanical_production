#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from math import ceil
from typing import Optional, Union

from design_of_mechanical_production.core.entities.types import IEquipment, IMachineInfo


@dataclass
class MachineInfo(IMachineInfo):
    """
    Класс для хранения информации о станке в зоне.
    """

    model: Union[IEquipment, str]  # Название станка
    calculated_count: Decimal  # Расчетное количество станков
    actual_count: Optional[int] = None  # Фактическое количество станков

    def __post_init__(self) -> None:
        """
        Инициализирует фактическое количество станков после создания объекта.
        """
        self.actual_count = ceil(self.calculated_count)

    @property
    def accepted_count(self) -> int:
        """
        Возвращает принятое количество станков (округленное вверх).
        """
        return self.actual_count or ceil(self.calculated_count)
