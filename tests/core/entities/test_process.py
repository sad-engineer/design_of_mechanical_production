#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для класса Process.
"""
import unittest
from decimal import Decimal
from unittest.mock import MagicMock

from design_of_mechanical_production.core.entities import Process
from design_of_mechanical_production.core.interfaces import IOperation


class TestProcess(unittest.TestCase):
    """Тесты для класса Process."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.operation1 = MagicMock(spec=IOperation)
        self.operation1.time = Decimal("120")
        self.operation1.calculated_equipment_count = Decimal("1.5")
        self.operation1.accepted_equipment_count = 2
        self.operation1.load_factor = Decimal("0.75")
        self.operation1.percentage = None

        self.operation2 = MagicMock(spec=IOperation)
        self.operation2.time = Decimal("180")
        self.operation2.calculated_equipment_count = Decimal("2.5")
        self.operation2.accepted_equipment_count = 3
        self.operation2.load_factor = Decimal("0.83")
        self.operation2.percentage = None

        self.process = Process(operations=[self.operation1, self.operation2])

    def test_01_initialization(self):
        """Тест инициализации процесса."""
        self.assertEqual(self.process.operations, [self.operation1, self.operation2])

    def test_02_calculate_total_time(self):
        """Тест расчета общего времени."""
        self.assertEqual(self.process.total_time, Decimal("300"))  # 120 + 180 = 300

    def test_03_total_machines_count(self):
        """Тест расчета общего количества станков."""
        self.assertEqual(self.process.accepted_machines_count, 5)  # 2 + 3 = 5

    def test_04_calculated_machines_count(self):
        """Тест расчета общего расчетного количества станков."""
        self.assertEqual(self.process.calculated_machines_count, Decimal("4.0"))  # 1.5 + 2.5 = 4.0

    def test_05_average_load_factor(self):
        """Тест расчета среднего коэффициента загрузки."""
        self.assertEqual(self.process.average_load_factor, Decimal("0.79"))  # (0,75 + 0.83) / 2

    def test_06_average_load_factor_with_zero_accepted(self):
        """Тест расчета среднего коэффициента загрузки при нулевых средних значениях."""
        self.operation1.load_factor = 0
        self.operation2.load_factor = 0
        self.assertEqual(self.process.average_load_factor, Decimal("0"))

    def test_07_calculate_percentage(self):
        """Тест расчета процентного соотношения операций."""
        self.process.calculate_percentage()
        self.operation1.calculate_percentage.assert_called_once_with(Decimal("300"))
        self.operation2.calculate_percentage.assert_called_once_with(Decimal("300"))

    def test_08_add_operation(self):
        """Тест добавления операции."""
        new_operation = MagicMock(spec=IOperation)
        new_operation.time = Decimal("200")
        new_operation.calculated_equipment_count = Decimal("3.5")
        new_operation.accepted_equipment_count = 4
        new_operation.load_factor = Decimal("0.875")
        new_operation.percentage = None

        # Добавляем операцию
        self.process.add_operation(new_operation)

        # Проверяем, что операция добавлена
        self.assertEqual(self.process.operations[-1], new_operation)

        # Проверяем обновленные значения
        self.assertEqual(self.process.total_time, Decimal("500"))
        self.assertEqual(self.process.accepted_machines_count, 9)
        self.assertEqual(self.process.calculated_machines_count, Decimal("7.5"))
        self.assertEqual(self.process.average_load_factor, Decimal("0.8183333333333333333333333333"))

        # Проверяем, что calculate_percentage был вызван один раз для каждой операции
        self.operation1.calculate_percentage.assert_called_once_with(Decimal("500"))
        self.operation2.calculate_percentage.assert_called_once_with(Decimal("500"))
        new_operation.calculate_percentage.assert_called_once_with(Decimal("500"))

    def test_09_calculate_required_machines(self):
        """Тест расчета необходимого количества станков."""
        # Создаем мок для оборудования
        equipment_mock = MagicMock()
        equipment_mock.model = "Станок1"

        # Настраиваем мок для операции
        operation = MagicMock(spec=IOperation)
        operation.time = Decimal("120")
        operation.equipment = equipment_mock
        operation.calculated_equipment_count = Decimal("0")
        operation.accepted_equipment_count = 0

        process = Process(operations=[operation])
        process.calculate_required_machines(
            production_volume=1000, fund_of_working=2000, kv=Decimal("1.1"), kp=Decimal("1.2")
        )
        machines = process.machines

        # Проверяем результаты
        self.assertEqual(len(machines), 1)
        self.assertEqual(
            machines["Станок1"].calculated_count, Decimal("45.45454545454545454545454545")
        )  # (1000 * 120) / (2000 * 1.1 * 1.2)
        operation.accept_count.assert_called_once_with(Decimal("45.45454545454545454545454545"))


if __name__ == '__main__':
    unittest.main()
