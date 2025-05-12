#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from typing import Any, Dict, List

from design_of_mechanical_production.core.services.validation import (
    validate_parameters_data,
    validate_process_data,
)


# Тестовая функция для декораторов
@validate_parameters_data
@validate_process_data
def decorated_function(parameters_data: Dict[str, Any], process_data: List[Dict[str, Any]]) -> None:
    pass


class TestProcessDataValidation(unittest.TestCase):
    """Тесты для валидации данных технологического процесса."""

    def test_01_valid_process_data(self) -> None:
        """Тест с корректными данными процесса."""
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        valid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': 5.5}
        decorated_function(valid_parameters_data, valid_process_data)  # Не должно вызывать исключений

    def test_02_empty_process_data(self) -> None:
        """Тест с пустым списком операций."""
        valid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': 5.5}
        with self.assertRaisesRegex(ValueError, "Список операций не может быть пустым"):
            decorated_function(valid_parameters_data, [])

    def test_03_missing_required_fields(self) -> None:
        """Тест с отсутствующими обязательными полями."""
        valid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': 5.5}
        invalid_process_data = [
            {
                'number': 1,
                'name': 'Операция 1',
                'time': 10.5,
                # Отсутствует поле 'machine'
            }
        ]
        with self.assertRaisesRegex(ValueError, "Неполные данные операции"):
            decorated_function(valid_parameters_data, invalid_process_data)

    def test_04_negative_time(self) -> None:
        """Тест с отрицательным временем операции."""
        valid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': 5.5}
        invalid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': -10.5, 'machine': 'Станок 1'}]
        with self.assertRaisesRegex(ValueError, "Время операции должно быть положительным числом"):
            decorated_function(valid_parameters_data, invalid_process_data)


class TestParametersDataValidation(unittest.TestCase):
    """Тесты для валидации параметров цеха."""

    def test_01_valid_parameters_data(self) -> None:
        """Тест с корректными параметрами цеха."""
        valid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': 5.5}
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        decorated_function(valid_parameters_data, valid_process_data)  # Не должно вызывать исключений

    def test_02_empty_parameters_data(self) -> None:
        """Тест с пустыми параметрами цеха."""
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        with self.assertRaisesRegex(ValueError, "Параметры цеха не могут быть пустыми"):
            decorated_function({}, valid_process_data)

    def test_03_missing_required_fields(self) -> None:
        """Тест с отсутствующими обязательными полями."""
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        invalid_parameters_data = {
            'name': 'Цех 1',
            'production_volume': 1000.0,
            # Отсутствует поле 'mass_detail'
        }
        with self.assertRaisesRegex(ValueError, "Отсутствуют обязательные параметры"):
            decorated_function(invalid_parameters_data, valid_process_data)

    def test_04_negative_production_volume(self) -> None:
        """Тест с отрицательным объемом производства."""
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        invalid_parameters_data = {'name': 'Цех 1', 'production_volume': -1000.0, 'mass_detail': 5.5}
        with self.assertRaisesRegex(ValueError, "Объем производства должен быть положительным числом"):
            decorated_function(invalid_parameters_data, valid_process_data)

    def test_05_negative_mass_detail(self) -> None:
        """Тест с отрицательной массой детали."""
        valid_process_data = [{'number': 1, 'name': 'Операция 1', 'time': 10.5, 'machine': 'Станок 1'}]
        invalid_parameters_data = {'name': 'Цех 1', 'production_volume': 1000.0, 'mass_detail': -5.5}
        with self.assertRaisesRegex(ValueError, "Масса детали должна быть положительным числом"):
            decorated_function(invalid_parameters_data, valid_process_data)


if __name__ == '__main__':
    unittest.main()
