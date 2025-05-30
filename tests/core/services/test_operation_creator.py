#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from design_of_mechanical_production.core.entities import Operation
from design_of_mechanical_production.core.services.operation_creator import create_operations_from_data


class TestOperationCreator(unittest.TestCase):
    """Тесты для создания операций технологического процесса."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        patcher = patch(
            "design_of_mechanical_production.core.factories.equipment_factory.EquipmentFactory.create_equipment"
        )
        self.addCleanup(patcher.stop)
        self.mock_create_equipment = patcher.start()

        # Настраиваем мок для create_equipment
        mock_equipment = MagicMock()
        mock_equipment.model = "DMG CTX beta 2000"
        self.mock_create_equipment.return_value = mock_equipment

        self.valid_process_data = [
            {'number': "005", 'name': "Операция 1", 'time': 10.5, 'machine': "DMG CTX beta 2000"},
            {'number': "010", 'name': "Операция 2", 'time': 15.3, 'machine': "DMG CTX beta 2000"},
        ]
        self.single_operation_data = [
            {'number': "015", 'name': "Операция 1", 'time': 10.5, 'machine': "DMG CTX beta 2000"}
        ]

    def test_01_create_operations_with_valid_data(self) -> None:
        """Тест создания операций с корректными данными."""
        # Выполнение
        operations = create_operations_from_data(self.valid_process_data)

        # Проверка
        self.assertIsInstance(operations, list)
        self.assertEqual(len(operations), 2)

        # Проверка первой операции
        self.assertIsInstance(operations[0], Operation)
        self.assertEqual(operations[0].number, "005")
        self.assertEqual(operations[0].name, "Операция 1")
        self.assertEqual(operations[0].time, Decimal("10.5"))
        self.assertEqual(operations[0].equipment.model, "DMG CTX beta 2000")

        # Проверка второй операции
        self.assertIsInstance(operations[1], Operation)
        self.assertEqual(operations[1].number, "010")
        self.assertEqual(operations[1].name, "Операция 2")
        self.assertEqual(operations[1].time, Decimal("15.3"))
        self.assertEqual(operations[1].equipment.model, "DMG CTX beta 2000")

        # Проверка вызовов create_equipment
        self.assertEqual(self.mock_create_equipment.call_count, 2)
        self.mock_create_equipment.assert_any_call("DMG CTX beta 2000")

    def test_02_create_operations_with_single_operation(self) -> None:
        """Тест создания одной операции."""
        # Выполнение
        operations = create_operations_from_data(self.single_operation_data)

        # Проверка
        self.assertIsInstance(operations, list)
        self.assertEqual(len(operations), 1)

        # Проверка операции
        self.assertIsInstance(operations[0], Operation)
        self.assertEqual(operations[0].number, "015")
        self.assertEqual(operations[0].name, "Операция 1")
        self.assertEqual(operations[0].time, Decimal("10.5"))
        self.assertEqual(operations[0].equipment.model, "DMG CTX beta 2000")

        # Проверка вызова create_equipment
        self.mock_create_equipment.assert_called_once_with("DMG CTX beta 2000")

    def test_03_create_operations_with_empty_data(self) -> None:
        """Тест создания операций с пустым списком данных."""
        # Выполнение
        operations = create_operations_from_data([])

        # Проверка
        self.assertIsInstance(operations, list)
        self.assertEqual(len(operations), 0)
        self.mock_create_equipment.assert_not_called()

    def test_04_create_operations_with_invalid_machine(self) -> None:
        """Тест создания операций с несуществующей моделью станка."""
        invalid_data = [{'number': "005", 'name': "Операция 1", 'time': 10.5, 'machine': "Несуществующий станок"}]

        # Настраиваем мок для выброса исключения
        self.mock_create_equipment.side_effect = ValueError("Станок не найден")

        # Проверка
        with self.assertRaises(ValueError):
            create_operations_from_data(invalid_data)

    def test_05_create_operations_with_negative_time(self) -> None:
        """Тест создания операций с отрицательным временем."""
        invalid_data = [{'number': "005", 'name': "Операция 1", 'time': -10.5, 'machine': "DMG CTX beta 2000"}]

        # Проверка
        with self.assertRaises(ValueError):
            create_operations_from_data(invalid_data)


if __name__ == '__main__':
    unittest.main()
