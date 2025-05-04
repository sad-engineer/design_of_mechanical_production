#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Optional, Protocol, Union


class IMachineInfo(Protocol):
    """
    Интерфейс для информации о станке в зоне.

    Attributes:
    model: Название станка или объект оборудования
    calculated_count: Расчетное количество станков
    actual_count: Фактическое количество станков (может быть None)
    """

    model: Union[str, 'IEquipment']
    calculated_count: Decimal
    actual_count: Optional[int]

    @property
    def accepted_count(self) -> int:
        """
        Принятое количество станков.
        """
        return ...

    def __post_init__(self) -> None:
        """
        Инициализация после создания объекта.
        """
        ...
