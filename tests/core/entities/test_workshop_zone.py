#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для классов WorkshopZone и SpecificWorkshopZone.
"""
import unittest
from decimal import Decimal
from unittest.mock import Mock, patch

from design_of_mechanical_production.core.entities.workshop_zone import SpecificWorkshopZone, WorkshopZone
from design_of_mechanical_production.core.interfaces import IMachineInfo


class TestWorkshopZone(unittest.TestCase):
    """Тесты для класса WorkshopZone."""

    @classmethod
    def setUpClass(cls):
        """Подготовка тестовых данных на уровне класса."""
        cls.zone_name = "Основная зона"
        cls.patcher = patch('design_of_mechanical_production.core.entities.workshop_zone.get_setting')
        cls.mock_get_setting = cls.patcher.start()
        cls.mock_get_setting.return_value = '1.5'

    @classmethod
    def tearDownClass(cls):
        """Очистка после всех тестов."""
        cls.patcher.stop()

    def setUp(self):
        """Подготовка тестовых данных для каждого теста."""
        self.workshop_zone = WorkshopZone(name=self.zone_name)
        # Проверяем, что get_setting был вызван с правильным параметром
        self.mock_get_setting.assert_called_with('passage_area')

        # Создаем мок для IMachineInfo
        self.machine_mock = Mock(spec=IMachineInfo)
        self.machine_mock.calculated_count = Decimal('2.5')
        self.machine_mock.accepted_count = 3

        # Создаем мок для модели станка
        self.model_mock = Mock()
        self.model_mock.length = Decimal('2.0')
        self.model_mock.width = Decimal('1.0')
        self.machine_mock.model = self.model_mock

    def test_01_initialization(self):
        """Тест инициализации зоны."""
        self.assertEqual(self.workshop_zone.name, self.zone_name)
        self.assertEqual(self.workshop_zone.machines, {})

    def test_02_add_machine(self):
        """Тест добавления станка в зону."""
        machine_name = "Токарный станок"
        self.workshop_zone.add_machine(machine_name, self.machine_mock)
        self.assertIn(machine_name, self.workshop_zone.machines)
        self.assertEqual(self.workshop_zone.machines[machine_name], self.machine_mock)

    def test_03_calculated_machines_count(self):
        """Тест расчета общего количества станков."""
        self.workshop_zone.add_machine("Станок 1", self.machine_mock)
        self.workshop_zone.add_machine("Станок 2", self.machine_mock)
        expected_count = Decimal('5.0')  # 2.5 * 2
        self.assertEqual(self.workshop_zone.calculated_machines_count, expected_count)

    def test_04_accepted_machines_count(self):
        """Тест подсчета принятого количества станков."""
        self.workshop_zone.add_machine("Станок 1", self.machine_mock)
        self.workshop_zone.add_machine("Станок 2", self.machine_mock)
        expected_count = 6  # 3 * 2
        self.assertEqual(self.workshop_zone.accepted_machines_count, expected_count)

    def test_05_area_calculation(self):
        """Тест расчета площади зоны."""
        self.workshop_zone.add_machine("Станок 1", self.machine_mock)
        expected_area = (Decimal('2.0') * Decimal('1.0') + Decimal('1.5')) * 3
        self.assertEqual(self.workshop_zone.area, expected_area)


class TestSpecificWorkshopZone(unittest.TestCase):
    """Тесты для класса SpecificWorkshopZone."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.zone_name = "Вспомогательная зона"
        self.specific_area = Decimal('2.5')
        self.total_equipment_count = 5
        self.specific_zone = SpecificWorkshopZone(
            name=self.zone_name, specific_area=self.specific_area, unit_of_calculation=self.total_equipment_count
        )

    def test_01_initialization(self):
        """Тест инициализации вспомогательной зоны."""
        self.assertEqual(self.specific_zone.name, self.zone_name)
        self.assertEqual(self.specific_zone.specific_area, self.specific_area)
        self.assertEqual(self.specific_zone.unit_of_calculation, self.total_equipment_count)

    def test_02_area_calculation(self):
        """Тест расчета площади вспомогательной зоны."""
        expected_area = self.specific_area * self.total_equipment_count
        self.assertEqual(self.specific_zone.area, expected_area)

    def test_03_total_calculated_equipment_count(self):
        """Тест получения общего количества оборудования."""
        expected_count = Decimal(str(self.total_equipment_count))
        self.assertEqual(self.specific_zone.unit_of_calculation, expected_count)

    def test_04_decimal_equipment_count(self):
        """Тест работы с десятичным количеством оборудования."""
        decimal_count = Decimal('5.5')
        zone = SpecificWorkshopZone(
            name=self.zone_name, specific_area=self.specific_area, unit_of_calculation=decimal_count
        )
        expected_area = self.specific_area * decimal_count
        self.assertEqual(zone.area, expected_area)


if __name__ == '__main__':
    unittest.main()
