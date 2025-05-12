#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Any, Callable, Dict, List

from design_of_mechanical_production.core.entities import Operation
from design_of_mechanical_production.core.factories import EquipmentFactory


def create_operations_from_data(
    process_data: List[Dict[str, Any]], factory: Callable = EquipmentFactory
) -> List[Operation]:
    """
    Создает список операций из входных данных.

    Args:
        process_data: Список словарей с данными технологического процесса:
            - number: int - номер операции
            - name: str - название операции
            - time: float - время операции
            - machine: str - модель станка
        factory: Callable - фабрика для создания оборудования

    Returns:
        List[Operation]: Список созданных операций
    """
    # Создаем фабрику оборудования
    equipment_factory = factory()
    # Создаем список операций
    operations = []
    for op_data in process_data:
        equipment = equipment_factory.create_equipment(op_data['machine'])
        operation = Operation(
            number=op_data['number'], name=op_data['name'], time=Decimal(str(op_data['time'])), equipment=equipment
        )
        operations.append(operation)
    return operations
