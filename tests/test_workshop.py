#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для класса Workshop.
"""
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from design_of_mechanical_production.core.entities import EquipmentFactory, Operation, Process, Workshop, WorkshopZone


class TestWorkshop(unittest.TestCase):
    """Тесты для класса Workshop."""

    def setUp(self):
        """Подготовка тестовых данных."""
        patcher = patch("design_of_mechanical_production.core.entities.equipment_factory.EquipmentFactory.create_equipment")
        self.addCleanup(patcher.stop)
        self.mock_create_equipment = patcher.start()

        # Мокнутый станок
        fake_equipment = MagicMock()
        fake_equipment.name = "16К20"
        fake_equipment.length = Decimal("2795")
        fake_equipment.width = Decimal("1500")
        fake_equipment.height = Decimal("1190")
        fake_equipment.automation = "Ручной"
        fake_equipment.weight = Decimal("3005.0")
        fake_equipment.power_lathe_passport_kvt = Decimal("11.0")

        # Настроим мок возвращаемым значением
        self.mock_create_equipment.side_effect = lambda model: fake_equipment

        # Создаем мок для процесса
        self.operation1 = MagicMock(spec=Operation)
        self.operation1.time = Decimal("20")
        self.operation1.equipment = fake_equipment
        self.operation1.calculated_equipment_count = Decimal("3.5")
        self.operation1.accepted_equipment_count = 4
        self.operation1.load_factor = Decimal("0.875")
        self.operation1.percentage = None

        self.operation2 = MagicMock(spec=Operation)
        self.operation2.time = Decimal("80")
        self.operation2.calculated_equipment_count = Decimal("3.5")
        self.operation2.equipment = fake_equipment
        self.operation2.accepted_equipment_count = 4
        self.operation2.load_factor = Decimal("0.875")
        self.operation2.percentage = None

        self.process = Process(operations=[self.operation1, self.operation2])
        self.process.calculate_required_machines(production_volume=1000)

        # Создаем тестовый цех
        self.workshop = Workshop(
            name="Тестовый цех", production_volume=1000, mass_detail=Decimal("10.5"), process=self.process
        )

    def test_01_workshop_initialization(self):
        """Тест инициализации цеха."""
        self.assertEqual(self.workshop.name, "Тестовый цех")
        self.assertEqual(self.workshop.production_volume, 1000)
        self.assertEqual(self.workshop.mass_detail, Decimal("10.5"))
        self.assertEqual(self.workshop.process, self.process)
        self.assertIn('main_zone', self.workshop.zones)

    def test_02_total_machines_count(self):
        """Тест расчета общего количества станков."""
        self.assertEqual(self.workshop.total_machines_count, 17)
        # Настраиваем мок для зоны
        main_zone = MagicMock(spec=WorkshopZone)
        main_zone.accepted_machines_count = 5
        self.workshop.zones['main_zone'] = main_zone

    def test_03_add_zone(self):
        """Тест добавления зоны."""
        test_zone = MagicMock(spec=WorkshopZone)
        self.workshop.add_zone('test_zone', test_zone)

        self.assertIn('test_zone', self.workshop.zones)
        self.assertEqual(self.workshop.zones['test_zone'], test_zone)

    @patch('design_of_mechanical_production.core.entities.workshop.get_setting')
    def test_04_calculate_total_area(self, mock_get_setting):
        """Тест расчета общей площади цеха."""
        # Настраиваем мок для настроек
        mock_get_setting.side_effect = lambda x: {'workshop_span': 8, 'workshop_nam': 2}[x]

        # Устанавливаем длину цеха
        self.workshop.length = Decimal("30")

        # Сбрасываем кэшированное значение площади
        self.workshop._total_area = Decimal("0")

        # Проверяем расчет площади
        self.workshop._calculate_total_area()
        expected_area = Decimal("8") * Decimal("2") * Decimal("30")
        self.assertEqual(self.workshop.total_area, expected_area)

    def test_05_calculate_required_area(self):
        """Тест расчета требуемой площади."""
        # Настраиваем мок для зоны
        main_zone = MagicMock(spec=WorkshopZone)
        main_zone.area = Decimal("100.5")
        self.workshop.zones['main_zone'] = main_zone

        # Проверяем расчет требуемой площади
        self.assertEqual(self.workshop.required_area, Decimal("100.5"))

    def test_06_length_property(self):
        """Тест работы со свойством длины цеха."""
        test_length = Decimal("50")
        self.workshop.length = test_length
        self.assertEqual(self.workshop.length, test_length)

    @patch('design_of_mechanical_production.core.entities.workshop.get_setting')
    def test_07_default_calculate_length(self, mock_get_setting):
        """Тест расчета длины цеха по умолчанию."""
        # Настраиваем мок для настроек
        mock_get_setting.side_effect = lambda x: {'workshop_span': 8, 'workshop_nam': 2}[x]

        # Настраиваем мок для зоны
        main_zone = MagicMock(spec=WorkshopZone)
        main_zone.area = Decimal("1000")
        self.workshop.zones['main_zone'] = main_zone

        # Вызываем расчет длины
        self.workshop.default_calculate_length()

        # Проверяем, что длина рассчитана корректно
        self.assertEqual(self.workshop.length, Decimal("62.625"))


if __name__ == '__main__':
    unittest.main()
