#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для класса Equipment.
"""
import unittest
from decimal import Decimal

from design_of_mechanical_production.core.entities import Equipment


class TestEquipment(unittest.TestCase):
    """Тесты для класса Equipment."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.equipment = Equipment(
            name="Токарный станок",
            model="DMG CTX beta 2000",
            length=Decimal("2.5"),
            width=Decimal("1.5"),
            height=Decimal("2.0"),
            automation="ЧПУ",
            weight=Decimal("5000"),
            power_consumption=Decimal("15.5"),
        )

    def test_01_area_calculation(self):
        """Тест расчета площади оборудования."""
        expected_area = Decimal("2.5") * Decimal("1.5")
        self.assertEqual(self.equipment.area, expected_area)

    def test_02_power_property(self):
        """Тест свойства power."""
        self.assertEqual(self.equipment.power, Decimal("15.5"))

    def test_03_dimensions_property(self):
        """Тест свойства dimensions."""
        expected_dimensions = {'length': Decimal("2.5"), 'width': Decimal("1.5"), 'height': Decimal("2.0")}
        self.assertEqual(self.equipment.dimensions, expected_dimensions)

    def test_04_equipment_with_none_name(self):
        """Тест создания оборудования без имени."""
        equipment = Equipment(
            name=None,
            model="DMG CTX beta 2000",
            length=Decimal("2.5"),
            width=Decimal("1.5"),
            height=Decimal("2.0"),
            automation="ЧПУ",
            weight=Decimal("5000"),
            power_consumption=Decimal("15.5"),
        )
        self.assertIsNone(equipment.name)

    def test_05_equipment_with_zero_dimensions(self):
        """Тест создания оборудования с нулевыми размерами."""
        equipment = Equipment(
            name="Тестовый станок",
            model="Test Model",
            length=Decimal("0"),
            width=Decimal("0"),
            height=Decimal("0"),
            automation="Ручное",
            weight=Decimal("0"),
            power_consumption=Decimal("0"),
        )
        self.assertEqual(equipment.area, Decimal("0"))
        self.assertEqual(equipment.power, Decimal("0"))


if __name__ == '__main__':
    unittest.main()
