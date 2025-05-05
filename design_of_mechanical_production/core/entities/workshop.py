#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict

from design_of_mechanical_production.core.entities.workshop_zone import WorkshopZone
from design_of_mechanical_production.core.interfaces import (
    IProcess,
    IWorkshop,
    IWorkshopZone,
    ISpecificWorkshopZone,
)
from design_of_mechanical_production.settings import get_setting


@dataclass
class Workshop(IWorkshop):
    """
    Класс, представляющий машиностроительный цех.

    Создает цех на основе процесса и производственного объема.
    В состав включена основная зона, в которую добавляются станки в соответствии с процессом.
    """

    name: str
    production_volume: float
    mass_detail: Decimal
    process: IProcess
    zones: Dict[str, IWorkshopZone] = field(default_factory=dict)

    _total_area: Decimal = Decimal("0")
    _required_area: Decimal = Decimal("0")
    _length: Decimal = Decimal("0")

    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков в цехе.
        """
        total_count = 0
        for name, zone in self.zones.items():
            if hasattr(zone, 'accepted_machines_count'):
                total_count += zone.accepted_machines_count
        return total_count

    @property
    def total_area(self) -> Decimal:
        """
        Общая площадь цеха.
        """
        self._calculate_total_area()
        return self._total_area

    @property
    def required_area(self) -> Decimal:
        """
        Общая площадь цеха.
        """
        self._calculate_required_area()
        return self._required_area

    @property
    def length(self) -> Decimal:
        """
        Длина цеха.
        """
        return self._length

    @length.setter
    def length(self, value: Decimal) -> None:
        """
        Устанавливает длину цеха.
        """
        self._length = value

    def _calculate_total_area(self) -> None:
        """
        Рассчитывает общую площадь цеха.
        Итоговая площадь рассчитывается как (ширина пролета * количество пролетов) * длину пролета
        Длина пролета рассчитывается как required_area / (ширина пролета * количество пролетов)
        Общая площадь округляется в большую сторону до числа, кратного 6
        """
        # Получаем настройки из конфигурации
        width_span = Decimal(str(get_setting('workshop_span')))
        number_spans = Decimal(str(get_setting('workshop_nam')))
        self._total_area = (width_span * number_spans) * self._length

    def _calculate_required_area(self) -> None:
        """
        Рассчитывает общую площадь, занимаемую оборудованием.
        """
        total_required_area = Decimal("0")
        for zone in self.zones.values():
            # Суммируем площади с учетом количества станков
            total_required_area += zone.area
        self._required_area = total_required_area

    def add_zone(self, name: str, zone: IWorkshopZone | ISpecificWorkshopZone) -> None:
        """
        Добавляет зону в цех.

        Args:
            name: Название зоны
            zone: Объект зоны
        """
        self.zones[name] = zone

    def default_calculate_length(self) -> None:
        """
        Рассчитывает длину цеха по умолчанию.
        """
        total_area = 0
        # Получаем настройки из конфигурации
        width_span = Decimal(str(get_setting('workshop_span')))
        number_spans = Decimal(str(get_setting('workshop_nam')))

        remainder = self.required_area % 6
        if remainder != 0:
            total_area = self.required_area + (6 - remainder)

        self._total_area = total_area
        self.length = total_area / (width_span * number_spans)
