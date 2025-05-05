#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from design_of_mechanical_production.core.entities import Operation, Process


def create_process_from_data(production_volume: float, operations: List[Operation]) -> Process:
    """
    Создает объект технологического процесса из входных данных.

    Args:
        production_volume: Годовой объем производства (должен быть положительным числом)
        operations: Список операций

    Returns:
        Process: Созданный объект технологического процесса

    Raises:
        ValueError: Если входные данные некорректны
    """
    if production_volume <= 0:
        raise ValueError("Объем производства должен быть положительным числом")

    if not operations:
        raise ValueError("Список операций не может быть пустым")

    # Создаем технологический процесс
    process = Process()
    for operation in operations:
        process.add_operation(operation)
    process.calculate_required_machines(production_volume)
    return process
