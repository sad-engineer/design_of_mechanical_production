#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Any, Dict, List

from design_of_mechanical_production.core.entities import MachineInfo, Operation, Process, Workshop
from design_of_mechanical_production.core.factories import EquipmentFactory, WorkshopZoneFactory
from design_of_mechanical_production.core.services import create_operations_from_data, create_process_from_data
from design_of_mechanical_production.core.services.validation import (
    validate_operations,
    validate_parameters_data,
    validate_process_data,
    validate_production_volume,
)
from design_of_mechanical_production.settings import get_setting

# Константы для расчета зон
GRINDING_ZONE_PERCENT = Decimal(str(get_setting('grinding_zone_percent')))  # 5% от общего числа станков
REPAIR_ZONE_PERCENT = Decimal(str(get_setting('repair_zone_percent')))  # 2.5% от общего числа станков


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
    validate_parameters_data(parameters_data)
    validate_process_data(process_data)
    # Валидация входных данных
    if not parameters_data or not process_data:
        raise ValueError("Входные данные не могут быть пустыми")

    required_params = ['name', 'production_volume', 'mass_detail']
    if not all(param in parameters_data for param in required_params):
        raise ValueError(f"Отсутствуют обязательные параметры: {required_params}")

    if float(parameters_data['production_volume']) <= 0:
        raise ValueError("Объем производства должен быть положительным числом")

    if float(parameters_data['mass_detail']) <= 0:
        raise ValueError("Масса детали должна быть положительным числом")

    production_volume = float(parameters_data['production_volume'])

    # Создаем технологический процесс
    process = create_process_from_data(production_volume, create_operations_from_data(process_data))

    # Создаем цех с основной зоной
    workshop = Workshop(
        name=parameters_data['name'],
        production_volume=production_volume,
        mass_detail=Decimal(str(parameters_data['mass_detail'])),
        process=process,
    )

    # Создаем фабрику зон
    zone_factory = WorkshopZoneFactory()

    # Создаем и добавляем основную зону
    workshop.add_zone(*zone_factory.create_main_zone(process.machines))

    # Создаем и добавляем дополнительные зоны
    grinding_zone_machines_count = {
        "3В642": MachineInfo(
            model="Станок универсально-заточной 3В642",
            calculated_count=process.accepted_machines_count * GRINDING_ZONE_PERCENT,
        )
    }
    workshop.add_zone(*zone_factory.create_grinding_zone(grinding_zone_machines_count))
    repair_zone_machines_count = {
        "3В642": MachineInfo(
            model="Станок универсально-заточной 3В642",
            calculated_count=process.accepted_machines_count * REPAIR_ZONE_PERCENT,
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
