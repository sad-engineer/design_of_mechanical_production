#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для класса Operation.
"""
import unittest
from decimal import Decimal
from unittest.mock import MagicMock

from design_of_mechanical_production.core.entities import Operation


class TestOperation(unittest.TestCase):
    """Тесты для класса Operation."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.equipment = MagicMock()
        self.operation = Operation(
            number="005",
            name="Токарная обработка",
            time=Decimal("120"),
            equipment=self.equipment,
            calculated_equipment_count=Decimal("1.5"),
        )

    def test_01_operation_initialization(self):
        """Тест инициализации операции."""
        # Проверяем атрибуты
        self.assertEqual(self.operation.number, "005")
        self.assertEqual(self.operation.name, "Токарная обработка")
        self.assertEqual(self.operation.time, Decimal("120"))
        self.assertEqual(self.operation.equipment, self.equipment)
        self.assertEqual(self.operation.calculated_equipment_count, Decimal("1.5"))
        self.assertEqual(self.operation.accepted_equipment_count, 0)
        self.assertEqual(self.operation.load_factor, Decimal("0"))
        self.assertIsNone(self.operation.percentage)

    def test_02_operation_initialization_with_zero_time(self):
        """Тест инициализации операции с нулевым временем."""
        with self.assertRaises(ValueError) as context:
            Operation(number="005", name="Токарная обработка", time=Decimal("0"), equipment=self.equipment)
        self.assertEqual(str(context.exception), "Время операции должно быть положительным")

    def test_03_operation_initialization_with_negative_time(self):
        """Тест инициализации операции с отрицательным временем."""
        with self.assertRaises(ValueError) as context:
            Operation(number="005", name="Токарная обработка", time=Decimal("-120"), equipment=self.equipment)
        self.assertEqual(str(context.exception), "Время операции должно быть положительным")

    def test_04_accept_count(self):
        """Тест принятия количества станков."""
        # Вызываем метод с корректным значением
        self.operation.accept_count(Decimal("2"))

        # Проверяем результаты
        self.assertEqual(self.operation.accepted_equipment_count, 2)
        self.assertEqual(self.operation.load_factor, Decimal("0.75"))  # 1.5 / 2 = 0.75

    def test_05_accept_count_with_negative_value(self):
        """Тест принятия отрицательного количества станков."""
        with self.assertRaises(ValueError) as context:
            self.operation.accept_count(Decimal("-1"))
        self.assertEqual(str(context.exception), "Принятое количество оборудования не может быть отрицательным")

    def test_06_accept_count_with_less_than_calculated(self):
        """Тест принятия количества станков меньше расчетного."""
        with self.assertRaises(ValueError) as context:
            self.operation.accept_count(Decimal("1"))
        self.assertEqual(str(context.exception), "Принятое количество оборудования не может быть меньше расчетного")

    def test_07_calculate_load_factor_with_zero_accepted(self):
        """Тест расчета коэффициента загрузки при нулевом принятом количестве."""
        self.operation.calculated_equipment_count = Decimal("0")
        # Вызываем метод
        self.operation.accept_count(Decimal("0"))

        # Проверяем результаты
        self.assertEqual(self.operation.accepted_equipment_count, 0)
        self.assertEqual(self.operation.load_factor, Decimal("0"))

        self.operation.calculated_equipment_count = Decimal("1.5")

    def test_08_calculate_percentage(self):
        """Тест расчета процентного соотношения."""
        # Вызываем метод
        total_time = Decimal("240")
        self.operation.calculate_percentage(total_time)

        # Проверяем результаты
        self.assertEqual(self.operation.percentage, Decimal("50"))  # (120 / 240) * 100 = 50

    def test_09_calculate_percentage_with_zero_total_time(self):
        """Тест расчета процентного соотношения при нулевом общем времени."""
        total_time = Decimal("0")
        with self.assertRaises(ValueError) as context:
            self.operation.calculate_percentage(total_time)
        self.assertEqual(str(context.exception), "Общее время не может быть отрицательным или нулевым")

    def test_10_calculate_percentage_with_negative_total_time(self):
        """Тест расчета процентного соотношения при отрицательном общем времени."""
        total_time = Decimal("-240")
        with self.assertRaises(ValueError) as context:
            self.operation.calculate_percentage(total_time)
        self.assertEqual(str(context.exception), "Общее время не может быть отрицательным или нулевым")


if __name__ == '__main__':
    unittest.main()
