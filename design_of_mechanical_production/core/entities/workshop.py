#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List

from design_of_mechanical_production.core.entities.types import IEquipment, IMachineInfo, IProcess, IWorkshop, IWorkshopZone
from design_of_mechanical_production.settings import get_setting


@dataclass
class Workshop(IWorkshop):
    """
    Класс, представляющий машиностроительный цех.
    """

    name: str
    production_volume: float
    mass_detail: Decimal
    process: IProcess
    equipment_list: List[IEquipment] = field(default_factory=list)
    zones: Dict[str, IWorkshopZone] = field(default_factory=dict)
    total_area: Decimal = Decimal("0")
    required_area: Decimal = Decimal("0")
    length: Decimal = Decimal("0")

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

    def calculate_total_area(self) -> Decimal:
        """
        Рассчитывает общую площадь цеха.
        Итоговая площадь рассчитывается как (ширина пролета * количество пролетов) * длину пролета
        Длина пролета рассчитывается как required_area / (ширина пролета * количество пролетов)
        Общая площадь округляется в большую сторону до числа, кратного 6
        """
        # Получаем настройки из конфигурации
        width_span = Decimal(str(get_setting('workshop_span')))
        number_spans = Decimal(str(get_setting('workshop_nam')))

        # Рассчитываем длину пролета
        self.length = self.required_area / (width_span * number_spans)

        # Рассчитываем общую площадь
        total_area = width_span * number_spans * self.length

        # Округляем до ближайшего большего числа, кратного 6
        remainder = total_area % 6
        if remainder != 0:
            total_area = total_area + (6 - remainder)

        self.total_area = total_area
        return self.total_area

    def calculate_required_area(self) -> Decimal:
        """
        Рассчитывает общую площадь, занимаемую оборудованием.
        """
        total_required_area = Decimal("0")
        for zone in self.zones.values():
            # Суммируем площади с учетом количества станков
            total_required_area += zone.area
        self.required_area = total_required_area

        return total_required_area

    def add_equipment(self, equipment: IEquipment) -> None:
        """
        Добавляет оборудование в цех.
        """
        self.equipment_list.append(equipment)

    def get_equipment_count(self) -> Dict[str, IMachineInfo]:
        """
        Возвращает количество оборудования.
        """
        return self.process.calculate_required_machines(self.production_volume)

    def get_machines_count(self) -> Dict[str, int]:
        """
        Возвращает количество станков.
        """
        machines = self.get_equipment_count()
        return {name: info.accepted_count for name, info in machines.items()}

    def add_zone(self, name: str, zone: IWorkshopZone) -> None:
        """
        Добавляет зону в цех.

        Args:
            name: Название зоны
            zone: Объект зоны
        """
        self.zones[name] = zone
