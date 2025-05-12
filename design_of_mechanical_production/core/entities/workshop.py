#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Optional

from design_of_mechanical_production.core.interfaces import (
    IProcess,
    ISpecificWorkshopZone,
    IWorkshop,
    IWorkshopZone,
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
    process_for_one_detail: IProcess  # процесс на одну деталь
    process_for_program: Optional[IProcess] = None  # процесс на производственную программу
    zones: Dict[str, IWorkshopZone] = field(default_factory=dict)
    length: Decimal = Decimal("0")

    _total_area: Decimal = Decimal("0")
    _required_area: Decimal = Decimal("0")
    _calculated_length: Decimal = Decimal("0")

    def __post_init__(self) -> None:
        """
        После инициализации цеха, расчитывается технологический процесс на производственную программу.
        """
        self.recalculate_process_for_program()

    def recalculate_process_for_program(self) -> None:
        """
        Пересчитывает технологический процесс на производственную программу.
        """
        self.process_for_program = copy.deepcopy(self.process_for_one_detail)
        for operation in self.process_for_program.operations:
            operation.time = operation.time * Decimal(str(self.production_volume))
        self.process.calculate_required_machines()

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
    def required_area_main_zone(self) -> Decimal:
        """
        Общая площадь основных зон цеха.
        """
        total_area = Decimal("0")
        for zone in self.zones.values():
            if zone.tokens["group"] == "main":
                total_area += zone.area
        return total_area

    @property
    def required_area_additional_zones(self) -> Decimal:
        """
        Общая площадь дополнительных зон цеха.
        """
        total_area = Decimal("0")
        for zone in self.zones.values():
            if zone.tokens["group"] == "additional":
                total_area += zone.area
        return total_area

    @property
    def calculated_length(self) -> Decimal:
        """
        Длина цеха.
        """
        return self._calculated_length

    @calculated_length.setter
    def calculated_length(self, value: Decimal) -> None:
        """
        Устанавливает длину цеха.
        """
        self._calculated_length = value

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
        self._total_area = (width_span * number_spans) * self.length

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
        # Получаем настройки из конфигурации
        width_span = Decimal(str(get_setting('workshop_span')))
        number_spans = Decimal(str(get_setting('workshop_nam')))

        self.calculated_length = self.required_area / (width_span * number_spans)
        remainder = self.calculated_length % 6
        if self.calculated_length != 0:
            self.length = self.calculated_length + (6 - remainder)

    @property
    def process(self) -> IProcess:
        """
        Возвращает технологический процесс (на производственную программу).
        """
        return self.process_for_program
