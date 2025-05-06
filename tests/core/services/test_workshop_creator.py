#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock

from design_of_mechanical_production.core.entities import Workshop
from design_of_mechanical_production.core.services.workshop_creator import create_workshop_from_data


class TestWorkshopCreator(unittest.TestCase):
    """Тесты для создания цеха."""

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

        self.valid_parameters_data = {'name': "Цех №1", 'production_volume': 1000.0, 'mass_detail': 10.5}
        self.valid_process_data = [
            {'number': "005", 'name': "Операция 1", 'time': 10.5, 'machine': "DMG CTX beta 2000"},
            {'number': "010", 'name': "Операция 2", 'time': 15.3, 'machine': "DMG CTX beta 2000"},
        ]

    def test_01_create_workshop_with_valid_data(self) -> None:
        """Тест создания цеха с корректными данными."""
        # Выполнение
        workshop = create_workshop_from_data(self.valid_parameters_data, self.valid_process_data)

        # Проверка
        self.assertIsInstance(workshop, Workshop)
        self.assertEqual(workshop.name, "Цех №1")
        self.assertEqual(workshop.production_volume, 1000.0)
        self.assertEqual(workshop.mass_detail, Decimal("10.5"))

        # Проверка наличия всех зон
        self.assertIn('main_zone', workshop.zones)
        self.assertIn('grinding_zone', workshop.zones)
        self.assertIn('repair_zone', workshop.zones)
        self.assertIn('tool_storage_zone', workshop.zones)
        self.assertIn('equipment_warehouse_zone', workshop.zones)
        self.assertIn('work_piece_storage_zone', workshop.zones)
        self.assertIn('control_department_zone', workshop.zones)
        self.assertIn('sanitary_zone', workshop.zones)

        # Проверка технологического процесса
        self.assertEqual(len(workshop.process.operations), 2)
        self.assertEqual(workshop.process.operations[0].number, "005")
        self.assertEqual(workshop.process.operations[1].number, "010")

        # Проверка вызовов create_equipment
        self.assertEqual(self.mock_create_equipment.call_count, 2)
        self.mock_create_equipment.assert_any_call("DMG CTX beta 2000")

    def test_02_create_workshop_with_empty_process_data(self) -> None:
        """Тест создания цеха с пустым списком операций."""
        # Проверка
        with self.assertRaises(ValueError):
            create_workshop_from_data(self.valid_parameters_data, [])

    def test_03_create_workshop_with_missing_parameters(self) -> None:
        """Тест создания цеха с отсутствующими параметрами."""
        invalid_parameters = {
            'name': "Цех №1",
            'production_volume': 1000.0,
            # Отсутствует mass_detail
        }

        # Проверка
        with self.assertRaises(ValueError):
            create_workshop_from_data(invalid_parameters, self.valid_process_data)

    def test_04_create_workshop_with_negative_production_volume(self) -> None:
        """Тест создания цеха с отрицательным объемом производства."""
        invalid_parameters = {'name': "Цех №1", 'production_volume': -1000.0, 'mass_detail': 10.5}

        # Проверка
        with self.assertRaises(ValueError):
            create_workshop_from_data(invalid_parameters, self.valid_process_data)

    def test_05_create_workshop_with_negative_mass_detail(self) -> None:
        """Тест создания цеха с отрицательной массой детали."""
        invalid_parameters = {'name': "Цех №1", 'production_volume': 1000.0, 'mass_detail': -10.5}

        # Проверка
        with self.assertRaises(ValueError):
            create_workshop_from_data(invalid_parameters, self.valid_process_data)

    def test_06_create_workshop_with_invalid_machine(self) -> None:
        """Тест создания цеха с несуществующей моделью станка."""
        invalid_process_data = [
            {'number': "005", 'name': "Операция 1", 'time': 10.5, 'machine': "Несуществующий станок"}
        ]

        # Настраиваем мок для выброса исключения
        self.mock_create_equipment.side_effect = ValueError("Станок не найден")

        # Проверка
        with self.assertRaises(ValueError):
            create_workshop_from_data(self.valid_parameters_data, invalid_process_data)


if __name__ == '__main__':
    unittest.main()
