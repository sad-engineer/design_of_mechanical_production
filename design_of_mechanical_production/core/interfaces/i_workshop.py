#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Protocol


class IWorkshop(Protocol):
    """
    Интерфейс для цеха.
    """

    name: str
    production_volume: float
    mass_detail: Decimal
    process: 'IProcess'
    zones: Dict[str, 'IWorkshopZone']
    length: Decimal
    _total_area: Decimal
    _required_area: Decimal
    _calculated_length: Decimal

    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков в цехе.
        """
        return ...

    @property
    def total_area(self) -> Decimal:
        """
        Общая площадь цеха.
        """
        return ...

    @property
    def required_area(self) -> Decimal:
        """
        Общая площадь цеха.
        """
        return ...

    @property
    def required_area_main_zone(self) -> Decimal:
        """
        Общая площадь основных зон цеха.
        """
        return ...

    @property
    def required_area_additional_zones(self) -> Decimal:
        """
        Общая площадь дополнительных зон цеха.
        """
        return ...

    @property
    def calculated_length(self) -> Decimal:
        """
        Длина цеха.
        """
        return ...

    @calculated_length.setter
    def calculated_length(self, value: Decimal) -> None:
        """
        Устанавливает длину цеха.
        """
        ...

    def _calculate_total_area(self) -> None:
        """
        Рассчитывает общую площадь цеха.
        """
        ...

    def _calculate_required_area(self) -> None:
        """
        Рассчитывает общую площадь, занимаемую оборудованием.
        """
        ...

    def add_zone(self, name: str, zone: 'IWorkshopZone') -> None:
        """
        Добавляет зону в цех.

        Args:
            name: Название зоны
            zone: Объект зоны
        """
        ...

    @property
    def process(self) -> 'IProcess':
        """
        Возвращает технологический процесс (на производственную программу).
        """
        return ...
