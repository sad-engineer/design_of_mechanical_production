#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from decimal import Decimal

from design_of_mechanical_production.core.entities import Equipment, Operation, Process
from design_of_mechanical_production.core.services.process_creator import create_process_from_data


class TestProcessCreator(unittest.TestCase):
    """Тесты для создания технологического процесса."""

    def setUp(self) -> None:
        """Подготовка тестовых данных."""
        self.operations = [
            Operation(
                number="005",
                name="Операция 1",
                time=Decimal("10.5"),
                equipment=Equipment(
                    name="Станок 1",
                    model="Станок 1",
                    length=Decimal("2.0"),
                    width=Decimal("1.0"),
                    height=Decimal("1.5"),
                    automation="Автоматический",
                    weight=Decimal("1000.0"),
                    power_consumption=Decimal("10.0"),
                ),
            ),
            Operation(
                number="010",
                name="Операция 2",
                time=Decimal("15.3"),
                equipment=Equipment(
                    name="Станок 2",
                    model="Станок 2",
                    length=Decimal("2.0"),
                    width=Decimal("1.0"),
                    height=Decimal("1.5"),
                    automation="Автоматический",
                    weight=Decimal("1000.0"),
                    power_consumption=Decimal("10.0"),
                ),
            ),
        ]
        self.single_operation = [
            Operation(
                number="015",
                name="Операция 1",
                time=Decimal("10.5"),
                equipment=Equipment(
                    name="Станок 1",
                    model="Станок 1",
                    length=Decimal("2.0"),
                    width=Decimal("1.0"),
                    height=Decimal("1.5"),
                    automation="Автоматический",
                    weight=Decimal("1000.0"),
                    power_consumption=Decimal("10.0"),
                ),
            )
        ]

    def test_01_create_process_with_valid_data(self) -> None:
        """Тест создания процесса с корректными данными."""
        # Выполнение
        process = create_process_from_data(self.operations)

        # Проверка
        self.assertIsInstance(process, Process)
        self.assertEqual(len(process.operations), 2)
        self.assertEqual(process.operations[0].number, "005")
        self.assertEqual(process.operations[1].number, "010")
        self.assertEqual(process.operations[0].name, "Операция 1")
        self.assertEqual(process.operations[1].name, "Операция 2")
        self.assertEqual(process.operations[0].time, Decimal("10.5"))
        self.assertEqual(process.operations[1].time, Decimal("15.3"))
        self.assertEqual(process.operations[0].equipment.model, "Станок 1")
        self.assertEqual(process.operations[1].equipment.model, "Станок 2")

    def test_02_create_process_with_empty_operations(self) -> None:
        """Тест создания процесса с пустым списком операций."""
        # Выполнение
        process = create_process_from_data([])

        # Проверка
        self.assertIsInstance(process, Process)
        self.assertEqual(len(process.operations), 0)

    def test_03_create_process_with_single_operation(self) -> None:
        """Тест создания процесса с одной операцией."""
        # Выполнение
        process = create_process_from_data(self.single_operation)

        # Проверка
        self.assertIsInstance(process, Process)
        self.assertEqual(len(process.operations), 1)
        self.assertEqual(process.operations[0].number, "015")
        self.assertEqual(process.operations[0].name, "Операция 1")
        self.assertEqual(process.operations[0].time, Decimal("10.5"))
        self.assertEqual(process.operations[0].equipment.model, "Станок 1")


if __name__ == '__main__':
    unittest.main()
