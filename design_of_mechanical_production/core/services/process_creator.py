#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from design_of_mechanical_production.core.entities import Operation, Process


def create_process_from_data(operations: List[Operation]) -> Process:
    """
    Создает объект технологического процесса из входных данных.

    Args:
        operations: Список операций

    Returns:
        Process: Созданный объект технологического процесса
    """
    # Создаем технологический процесс
    process = Process()
    for operation in operations:
        process.add_operation(operation)
    process.calculate_required_machines()
    return process
