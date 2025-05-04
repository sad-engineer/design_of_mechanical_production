#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Protocol


class IWorkshopZone(Protocol):
    """
    Интерфейс для зоны цеха.
    """

    name: str
    machines: Dict[str, 'IMachineInfo']

    def calculate_area(self) -> Decimal:
        """
        Рассчитывает площадь зоны.
        """
        ...

    def add_machine(self, name: str, machine: 'IMachineInfo') -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        ...

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Расчетное количество станков.
        """
        return ...

    @property
    def accepted_machines_count(self) -> int:
        """
        Принятое количество станков.
        """
        return ...

    @property
    def area(self) -> Decimal:
        """
        Площадь зоны.
        """
        return ...
