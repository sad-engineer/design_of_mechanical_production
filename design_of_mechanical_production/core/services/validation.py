#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from functools import wraps
from typing import Any, Callable


def validate_process_data(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        process_data = kwargs.get('process_data') or args[1]
        if not process_data:
            raise ValueError("Список операций не может быть пустым")
        for op_data in process_data:
            if not all(key in op_data for key in ['number', 'name', 'time', 'machine']):
                raise ValueError(f"Неполные данные операции: {op_data}")
            if float(op_data['time']) <= 0:
                raise ValueError(f"Время операции должно быть положительным числом: {op_data['time']}")
        return func(*args, **kwargs)

    return wrapper


def validate_parameters_data(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        parameters_data = kwargs.get('parameters_data') or args[0]
        if not parameters_data:
            raise ValueError("Параметры цеха не могут быть пустыми")
        required_params = ['name', 'production_volume', 'mass_detail']
        if not all(param in parameters_data for param in required_params):
            raise ValueError(f"Отсутствуют обязательные параметры: {required_params}")
        if float(parameters_data['production_volume']) <= 0:
            raise ValueError("Объем производства должен быть положительным числом")
        if float(parameters_data['mass_detail']) <= 0:
            raise ValueError("Масса детали должна быть положительным числом")
        return func(*args, **kwargs)

    return wrapper
