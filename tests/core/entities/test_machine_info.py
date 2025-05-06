#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для класса MachineInfo.
"""
import unittest
from decimal import Decimal
from math import ceil

from design_of_mechanical_production.core.entities import Equipment, MachineInfo


class TestMachineInfo(unittest.TestCase):
    """Тесты для класса MachineInfo."""

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

    def test_01_machine_info_with_equipment(self):
        """Тест создания MachineInfo с объектом Equipment."""
        calculated_count = Decimal("2.5")
        machine_info = MachineInfo(model=self.equipment, calculated_count=calculated_count)

        self.assertEqual(machine_info.model, self.equipment)
        self.assertEqual(machine_info.calculated_count, calculated_count)
        self.assertEqual(machine_info.accepted_count, ceil(calculated_count))

    def test_02_machine_info_with_string_model(self):
        """Тест создания MachineInfo со строковым названием модели."""
        model_name = "DMG CTX beta 2000"
        calculated_count = Decimal("3.7")
        machine_info = MachineInfo(model=model_name, calculated_count=calculated_count)

        self.assertEqual(machine_info.model, model_name)
        self.assertEqual(machine_info.calculated_count, calculated_count)
        self.assertEqual(machine_info.accepted_count, ceil(calculated_count))

    def test_03_machine_info_with_zero_count(self):
        """Тест создания MachineInfo с нулевым количеством станков."""
        machine_info = MachineInfo(model=self.equipment, calculated_count=Decimal("0"))

        self.assertEqual(machine_info.calculated_count, Decimal("0"))
        self.assertEqual(machine_info.accepted_count, 0)

    def test_04_machine_info_with_negative_count(self):
        """Тест создания MachineInfo с отрицательным количеством станков."""
        with self.assertRaises(ValueError) as context:
            MachineInfo(model=self.equipment, calculated_count=Decimal("-1.5"))
        self.assertEqual(str(context.exception), "Количество станков не может быть отрицательным")

    def test_05_machine_info_with_fractional_count(self):
        """Тест создания MachineInfo с дробным количеством станков."""
        calculated_count = Decimal("2.1")
        machine_info = MachineInfo(model=self.equipment, calculated_count=calculated_count)

        self.assertEqual(machine_info.calculated_count, calculated_count)
        self.assertEqual(machine_info.accepted_count, 3)  # Округление вверх


if __name__ == '__main__':
    unittest.main()
