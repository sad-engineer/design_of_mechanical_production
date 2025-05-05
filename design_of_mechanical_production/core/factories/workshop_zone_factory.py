#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Dict

from design_of_mechanical_production.core.entities import (
    SpecificWorkshopZone,
    WorkshopZone,
)
from design_of_mechanical_production.core.factories import EquipmentFactory
from design_of_mechanical_production.core.interfaces import IMachineInfo, ISpecificWorkshopZone, IWorkshopZone
from design_of_mechanical_production.settings import get_setting


class WorkshopZoneFactory:
    """
    Фабрика для создания различных типов зон цеха.
    """

    def __init__(self):
        """Инициализация фабрики."""
        self.equipment_factory = EquipmentFactory()

    @staticmethod
    def create_main_zone(machines: Dict[str, IMachineInfo]) -> tuple[str, IWorkshopZone]:
        """
        Создает основную зону цеха.
        Основная зона не знает про состав и количество станков, определим это во внешнем скрипте

        Args:
            machines: Словарь со станками и их количеством

        Returns:
            WorkshopZone: Созданная основная зона
        """
        workshop_zone = WorkshopZone(name='Основная зона')
        for machine_name, machine_info in machines.items():
            workshop_zone.add_machine(machine_name, machine_info)
        return 'main_zone', workshop_zone

    @staticmethod
    def create_grinding_zone(machines: Dict[str, IMachineInfo]) -> tuple[str, IWorkshopZone]:
        """
        Создает зону заточного отделения.
        Зона не знает про состав и количество станков, определим это во внешнем скрипте

        Args:
            machines: Словарь со станками и их количеством

        Returns:
            WorkshopZone: Созданная зона заточного отделения
        """
        workshop_zone = WorkshopZone(name='Заточное отделение')
        for machine_name, machine_info in machines.items():
            workshop_zone.add_machine(machine_name, machine_info)
        return 'grinding_zone', workshop_zone

    @staticmethod
    def create_repair_zone(machines: Dict[str, IMachineInfo]) -> tuple[str, IWorkshopZone]:
        """
        Создает зону ремонтного отделения.
        Зона не знает про состав и количество станков, определим это во внешнем скрипте

        Args:
            machines: Словарь со станками и их количеством

        Returns:
            WorkshopZone: Созданная зона ремонтного отделения
        """
        workshop_zone = WorkshopZone(name='Ремонтное отделение')
        for machine_name, machine_info in machines.items():
            workshop_zone.add_machine(machine_name, machine_info)
        return 'repair_zone', workshop_zone

    @staticmethod
    def create_tool_storage_zone(total_machines_count: int) -> tuple[str, ISpecificWorkshopZone]:
        """
        Создает зону склада инструмента.
        Зона определяется по правилу: 0.3м2 * total_machines_count
        * 0.3м2 - значение по умолчанию, может быть изменено в настройках расчета

        Args:
            total_machines_count: Общее количество станков

        Returns:
            SpecificWorkshopZone: Созданная зона склада инструмента
        """
        workshop_zone = SpecificWorkshopZone(
            name='Склад инструмента',
            specific_area=Decimal(str(get_setting('specific_areas.tool_storage'))),
            unit_of_calculation=total_machines_count,
        )
        return 'tool_storage_zone', workshop_zone

    @staticmethod
    def create_equipment_warehouse_zone(total_machines_count: int) -> tuple[str, ISpecificWorkshopZone]:
        """
        Создает зону склада приспособлений.
        Зона определяется по правилу: 0.2м2 * total_machines_count
        * 0.2м2 - значение по умолчанию, может быть изменено в настройках расчета

        Args:
            total_machines_count: Общее количество станков

        Returns:
            SpecificWorkshopZone: Созданная зона склада приспособлений
        """
        workshop_zone = SpecificWorkshopZone(
            name='Склад приспособлений',
            specific_area=Decimal(str(get_setting('specific_areas.equipment_warehouse'))),
            unit_of_calculation=total_machines_count,
        )
        return 'equipment_warehouse_zone', workshop_zone

    @staticmethod
    def create_work_piece_storage_zone(main_zone_area: Decimal) -> tuple[str, ISpecificWorkshopZone]:
        """
        Создает зону склада заготовок.
        Зона определяется по правилу: 30%* от общей площади основной зоны
        * - если не указано иное, в настройках расчета

        Args:
            main_zone_area: Площадь основной зоны

        Returns:
            SpecificWorkshopZone: Созданная зона склада заготовок
        """
        workshop_zone = SpecificWorkshopZone(
            name='Склад заготовок',
            specific_area=Decimal(str(get_setting('specific_areas.work_piece_storage'))),
            unit_of_calculation=main_zone_area,
        )
        return 'work_piece_storage_zone', workshop_zone

    @staticmethod
    def create_control_department_zone(main_zone_area: int) -> tuple[str, ISpecificWorkshopZone]:
        """
        Создает зону отделения контроля.
        Зона определяется по правилу: 0.05 * total_machines_count
        * 0.05 - значение по умолчанию, может быть изменено в настройках расчета

        Args:
            main_zone_area: Площадь основной зоны

        Returns:
            SpecificWorkshopZone: Созданная зона отделения контроля
        """
        workshop_zone = SpecificWorkshopZone(
            name='Отделение контроля',
            specific_area=Decimal(str(get_setting('specific_areas.control_department'))),
            unit_of_calculation=main_zone_area,
        )
        return 'control_department_zone', workshop_zone

    @staticmethod
    def create_sanitary_zone() -> tuple[str, ISpecificWorkshopZone]:
        """
        Создает санитарную зону.
        Зона определяется по правилу: 8м2 на каждый санузел (м/ж - 2 санузла)
        * 8 - значение по умолчанию, может быть изменено в настройках расчета

        Returns:
            SpecificWorkshopZone: Созданная санитарная зона
        """
        workshop_zone = SpecificWorkshopZone(
            name='Санитарная зона',
            specific_area=Decimal(str(get_setting('specific_areas.sanitary_zone'))),
            unit_of_calculation=2,
        )
        return 'sanitary_zone', workshop_zone
