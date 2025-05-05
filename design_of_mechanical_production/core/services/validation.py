#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List


def validate_process_data(process_data: List[Dict[str, Any]]) -> None:
    if not process_data:
        raise ValueError("Список операций не может быть пустым")
    for op_data in process_data:
        if not all(key in op_data for key in ['number', 'name', 'time', 'machine']):
            raise ValueError(f"Неполные данные операции: {op_data}")
        if float(op_data['time']) <= 0:
            raise ValueError(f"Время операции должно быть положительным числом: {op_data['time']}")


def validate_production_volume(production_volume: float) -> None:
    if production_volume <= 0:
        raise ValueError("Объем производства должен быть положительным числом")


def validate_operations(operations: List[Any]) -> None:
    if not operations:
        raise ValueError("Список операций не может быть пустым")


def validate_parameters_data(parameters_data: Dict[str, Any]) -> None:
    if not parameters_data:
        raise ValueError("Параметры цеха не могут быть пустыми")
    required_params = ['name', 'production_volume', 'mass_detail']
    if not all(param in parameters_data for param in required_params):
        raise ValueError(f"Отсутствуют обязательные параметры: {required_params}")
    if float(parameters_data['production_volume']) <= 0:
        raise ValueError("Объем производства должен быть положительным числом")
    if float(parameters_data['mass_detail']) <= 0:
        raise ValueError("Масса детали должна быть положительным числом")
