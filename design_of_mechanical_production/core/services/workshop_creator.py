#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Any, Dict, List

from design_of_mechanical_production.core.entities import MachineInfo, Workshop
from design_of_mechanical_production.core.factories import WorkshopZoneFactory
from design_of_mechanical_production.core.services import create_operations_from_data, create_process_from_data
from design_of_mechanical_production.core.services.validation import (
    validate_parameters_data,
    validate_process_data,
)
from design_of_mechanical_production.settings import get_setting

# Константы для расчета зон
GRINDING_ZONE_PERCENT = Decimal(str(get_setting('grinding_zone_percent')))  # 5% от общего числа станков
REPAIR_ZONE_PERCENT = Decimal(str(get_setting('repair_zone_percent')))  # 2.5% от общего числа станков


@validate_parameters_data
@validate_process_data
def create_workshop_from_data(parameters_data: Dict[str, Any], process_data: List[Dict[str, Any]]) -> Workshop:
    """
    Создает объект цеха из входных данных.

    Args:
        parameters_data: Словарь с параметрами цеха:
            - name: str - название цеха
            - production_volume: float - годовой объем производства
            - mass_detail: float - масса детали
        process_data: Список словарей с данными технологического процесса:
            - number: int - номер операции
            - name: str - название операции
            - time: float - время операции
            - machine: str - модель станка

    Returns:
        Workshop: Созданный объект цеха

    Raises:
        ValueError: Если входные данные некорректны
    """
    # Создаем технологический процесс
    process = create_process_from_data(create_operations_from_data(process_data))

    # Создаем цех с основной зоной
    workshop = Workshop(
        name=parameters_data['name'],
        production_volume=Decimal(str((parameters_data['production_volume']))),
        mass_detail=Decimal(str(parameters_data['mass_detail'])),
        process_for_one_detail=process,
    )

    # Создаем фабрику зон
    zone_factory = WorkshopZoneFactory()

    # Создаем и добавляем основную зону
    workshop.add_zone(*zone_factory.create_main_zone(workshop.process.machines))

    # Создаем и добавляем дополнительные зоны
    grinding_zone_machines_count = {
        "3В642": MachineInfo(
            model="Станок универсально-заточной 3В642",
            calculated_count=workshop.process.accepted_machines_count * GRINDING_ZONE_PERCENT,
        )
    }
    workshop.add_zone(*zone_factory.create_grinding_zone(grinding_zone_machines_count))
    repair_zone_machines_count = {
        "3В642": MachineInfo(
            model="Станок универсально-заточной 3В642",
            calculated_count=workshop.process.accepted_machines_count * REPAIR_ZONE_PERCENT,
        )
    }
    workshop.add_zone(*zone_factory.create_repair_zone(repair_zone_machines_count))

    # Расчет общего количества станков
    total_machines_count = (
        workshop.zones['main_zone'].accepted_machines_count
        + workshop.zones['grinding_zone'].accepted_machines_count
        + workshop.zones['repair_zone'].accepted_machines_count
    )

    # Создаем и добавляем вспомогательные зоны
    workshop.add_zone(*zone_factory.create_tool_storage_zone(total_machines_count))
    workshop.add_zone(*zone_factory.create_equipment_warehouse_zone(total_machines_count))
    workshop.add_zone(*zone_factory.create_work_piece_storage_zone(workshop.zones['main_zone'].area))
    workshop.add_zone(*zone_factory.create_control_department_zone(total_machines_count))
    workshop.add_zone(*zone_factory.create_sanitary_zone())

    # Рассчитываем длину цеха по дефолтному варианту
    workshop.default_calculate_length()

    return workshop
