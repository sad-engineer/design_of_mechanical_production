#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Any, Dict, List

from design_of_mechanical_production.core.entities import EquipmentFactory, Operation, Process, Workshop
from design_of_mechanical_production.core.entities.machine_info import MachineInfo
from design_of_mechanical_production.core.entities.types import MachineCountType
from design_of_mechanical_production.core.entities.workshop_zone import SpecificWorkshopZone, WorkshopZone
from design_of_mechanical_production.settings import get_setting


def create_workshop_from_data(parameters_data: Dict[str, Any], process_data: List[Dict[str, Any]]) -> Workshop:
    """
    Создает объект цеха из входных данных.

    Args:
        parameters_data: Данные параметров цеха
        process_data: Данные технологического процесса

    Returns:
        Workshop: Созданный объект цеха
    """
    # Создаем фабрику оборудования
    equipment_factory = EquipmentFactory()

    # Создаем список операций
    operations = []
    for op_data in process_data:
        equipment = equipment_factory.create_equipment(op_data['machine'])
        operation = Operation(number=op_data['number'], name=op_data['name'], time=Decimal(str(op_data['time'])), equipment=equipment)
        operations.append(operation)

    # Создаем технологический процесс
    production_volume = float(parameters_data['production_volume'])
    process = Process(operations=operations)
    process.calculate_percentage()
    machines_count: MachineCountType = process.calculate_required_machines(production_volume)

    # Создаем цех
    workshop = Workshop(name=parameters_data['name'], production_volume=production_volume, mass_detail=Decimal(str(parameters_data['mass_detail'])), process=process)

    # Создаем основную зону
    main_zone = WorkshopZone(
        name='Основная зона',
        machines=machines_count,
    )
    workshop.add_zone('main_zone', main_zone)

    # Расчет зоны заточного отделения (5% от общего числа станков)
    grinding_zone_percent = Decimal(str(get_setting('grinding_zone_percent')))
    grinding_zone = WorkshopZone(
        name='Заточное отделение',
        machines={"Станок универсально-заточной 3В642": MachineInfo(model=equipment_factory.create_equipment("3В642"), calculated_count=main_zone.total_equipment_count * grinding_zone_percent)},
    )
    workshop.add_zone('grinding_zone', grinding_zone)

    # Расчет зоны ремонтное отделение (25% от общего числа станков)
    repair_zone_percent = Decimal(str(get_setting('repair_zone_percent')))
    repair_zone = WorkshopZone(
        name='Ремонтное отделение',
        machines={"Станки в ремонте": MachineInfo(model="Станки в ремонте", calculated_count=main_zone.total_equipment_count * repair_zone_percent)},
    )
    workshop.add_zone('repair_zone', repair_zone)

    # Расчет вспомогательных зон
    total_machines_count = main_zone.total_equipment_count + grinding_zone.total_equipment_count + repair_zone.total_equipment_count

    # Склад инструмента
    tool_storage_zone = SpecificWorkshopZone(name='Склад инструмента', specific_area=Decimal(str(get_setting('specific_areas.tool_storage'))), total_equipment_count=total_machines_count)
    workshop.add_zone('tool_storage_zone', tool_storage_zone)

    # Склад приспособлений
    equipment_warehouse_zone = SpecificWorkshopZone(
        name='Склад приспособлений', specific_area=Decimal(str(get_setting('specific_areas.equipment_warehouse'))), total_equipment_count=total_machines_count
    )
    workshop.add_zone('equipment_warehouse_zone', equipment_warehouse_zone)

    # Склад заготовок
    work_piece_storage_zone = SpecificWorkshopZone(name='Склад заготовок', specific_area=Decimal(str(get_setting('specific_areas.work_piece_storage'))), total_equipment_count=main_zone.area)
    workshop.add_zone('work_piece_storage_zone', work_piece_storage_zone)

    # Отделение контроля
    control_department_zone = SpecificWorkshopZone(name='Отделение контроля', specific_area=Decimal(str(get_setting('specific_areas.control_department'))), total_equipment_count=total_machines_count)
    workshop.add_zone('control_department_zone', control_department_zone)

    # Санитарная зона
    sanitary_zone = SpecificWorkshopZone(name='Санитарная зона', specific_area=Decimal(str(get_setting('specific_areas.sanitary_zone'))), total_equipment_count=2)
    workshop.add_zone('sanitary_zone', sanitary_zone)

    # Рассчитываем требуемую площадь
    workshop.calculate_required_area()
    workshop.calculate_total_area()

    return workshop
