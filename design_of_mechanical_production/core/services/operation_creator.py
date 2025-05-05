#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Any, Dict, List

from design_of_mechanical_production.core.entities import Operation
from design_of_mechanical_production.core.factories import EquipmentFactory
from design_of_mechanical_production.core.services.validation import (
    validate_process_data,
)


def create_operations_from_data(process_data: List[Dict[str, Any]]) -> List[Operation]:
    """
    Создает список операций из входных данных.

    Args:
        process_data: Список словарей с данными технологического процесса:
            - number: int - номер операции
            - name: str - название операции
            - time: float - время операции
            - machine: str - модель станка

    Returns:
        List[Operation]: Список созданных операций

    Raises:
        ValueError: Если входные данные некорректны
    """
    validate_process_data(process_data)

    # Создаем фабрику оборудования
    equipment_factory = EquipmentFactory()
    # Создаем список операций
    operations = []
    for op_data in process_data:
        if not all(key in op_data for key in ['number', 'name', 'time', 'machine']):
            raise ValueError(f"Неполные данные операции: {op_data}")

        if float(op_data['time']) <= 0:
            raise ValueError(f"Время операции должно быть положительным числом: {op_data['time']}")

        equipment = equipment_factory.create_equipment(op_data['machine'])
        operation = Operation(
            number=op_data['number'], name=op_data['name'], time=Decimal(str(op_data['time'])), equipment=equipment
        )
        operations.append(operation)
    return operations
