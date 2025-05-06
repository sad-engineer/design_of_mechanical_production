#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для классов AreaCalculator и SpecificAreaCalculator.
"""
import unittest
from decimal import Decimal
from unittest.mock import Mock

from design_of_mechanical_production.core.entities.area_calculator import AreaCalculator, SpecificAreaCalculator
from design_of_mechanical_production.core.interfaces import IMachineInfo


class TestAreaCalculator(unittest.TestCase):
    """Тесты для класса AreaCalculator."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.passage_area = Decimal('1.5')
        self.calculator = AreaCalculator(self.passage_area)

        # Создаем мок для IMachineInfo
        self.machine_mock = Mock(spec=IMachineInfo)
        self.machine_mock.accepted_count = 2

        # Создаем мок для модели станка
        self.model_mock = Mock()
        self.model_mock.length = Decimal('2.0')
        self.model_mock.width = Decimal('1.0')
        self.machine_mock.model = self.model_mock

    def test_01_calculate_area_with_model_dimensions(self):
        """Тест расчета площади с размерами модели."""
        machines = {'machine1': self.machine_mock}
        expected_area = (Decimal('2.0') * Decimal('1.0') + self.passage_area) * 2
        self.assertEqual(self.calculator.calculate_area(machines), expected_area)

    def test_02_calculate_area_without_model_dimensions(self):
        """Тест расчета площади без размеров модели."""
        # Создаем мок без атрибутов length и width
        machine_mock = Mock(spec=IMachineInfo)
        machine_mock.accepted_count = 1

        # Создаем мок для модели станка без атрибутов length и width
        model_mock = Mock()
        # Удаляем атрибуты length и width
        delattr(model_mock, 'length')
        delattr(model_mock, 'width')
        machine_mock.model = model_mock

        machines = {'machine1': machine_mock}
        expected_area = (Decimal('2.000') * Decimal('1.000') + self.passage_area) * 1
        self.assertEqual(self.calculator.calculate_area(machines), expected_area)

    def test_03_calculate_area_with_multiple_machines(self):
        """Тест расчета площади для нескольких станков."""
        machines = {'machine1': self.machine_mock, 'machine2': self.machine_mock}
        expected_area = (Decimal('2.0') * Decimal('1.0') + self.passage_area) * 4  # 2 станка * 2 accepted_count
        self.assertEqual(self.calculator.calculate_area(machines), expected_area)


class TestSpecificAreaCalculator(unittest.TestCase):
    """Тесты для класса SpecificAreaCalculator."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.specific_area = Decimal('2.5')
        self.total_equipment_count = 5
        self.calculator = SpecificAreaCalculator(self.specific_area, self.total_equipment_count)

    def test_01_calculate_area_with_integer_count(self):
        """Тест расчета площади с целочисленным количеством оборудования."""
        machines = {'machine1': Mock(spec=IMachineInfo)}
        expected_area = self.specific_area * self.total_equipment_count
        self.assertEqual(self.calculator.calculate_area(machines), expected_area)

    def test_02_calculate_area_with_decimal_count(self):
        """Тест расчета площади с десятичным количеством оборудования."""
        calculator = SpecificAreaCalculator(self.specific_area, Decimal('5.5'))
        machines = {'machine1': Mock(spec=IMachineInfo)}
        expected_area = self.specific_area * Decimal('5.5')
        self.assertEqual(calculator.calculate_area(machines), expected_area)

    def test_03_calculate_area_with_zero_count(self):
        """Тест расчета площади с нулевым количеством оборудования."""
        calculator = SpecificAreaCalculator(self.specific_area, 0)
        machines = {'machine1': Mock(spec=IMachineInfo)}
        expected_area = self.specific_area * 0
        self.assertEqual(calculator.calculate_area(machines), expected_area)


if __name__ == '__main__':
    unittest.main()
