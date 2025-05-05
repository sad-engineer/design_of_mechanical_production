#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Тесты для классов MachineToolSource.
"""
import unittest
from unittest.mock import patch, MagicMock

from decimal import Decimal

from design_of_mechanical_production.core.entities.machine_tool_source import (
    DatabaseMachineToolSource,
    DefaultMachineToolSource,
    MachineTool,
    MachineToolSource,
)


class TestMachineToolSource(unittest.TestCase):
    """Тесты для базового класса MachineToolSource."""

    def test_01_base_class_raises_not_implemented(self):
        """Тест, что базовый класс вызывает NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            MachineToolSource.get_machine_tool("test_model")


class TestDatabaseMachineToolSource(unittest.TestCase):
    """Тесты для класса DatabaseMachineToolSource."""

    def setUp(self):
        self.test_model = "16К20"
        self.source = DatabaseMachineToolSource()

    @patch("design_of_mechanical_production.core.entities.machine_tool_source.Container")
    def test_01_get_machine_tool_success(self, mock_container_class):
        """Тест успешного получения данных о станке из БД (мокаем доступ)."""
        fake_tool = MagicMock()
        fake_tool.name = self.test_model
        fake_tool.length = "2795"
        fake_tool.width = "1500"
        fake_tool.height = "1190"
        fake_tool.automation = "Ручной"
        fake_tool.weight = "3005.0"
        fake_tool.power_lathe_passport_kvt = "11.0"

        mock_creator = MagicMock()
        mock_creator.by_name.return_value = fake_tool
        mock_container_class.return_value.creator.return_value = mock_creator

        result = self.source.get_machine_tool(self.test_model)

        self.assertEqual(result.name, self.test_model)
        self.assertEqual(result.length, "2795")
        self.assertEqual(result.width, "1500")
        self.assertEqual(result.height, "1190")
        self.assertEqual(result.automation, "Ручной")
        self.assertEqual(result.weight, "3005.0")
        self.assertEqual(result.power_lathe_passport_kvt, "11.0")

    @patch("design_of_mechanical_production.core.entities.machine_tool_source.Container")
    def test_02_get_machine_tool_not_found(self, mock_container_class):
        """Тест обработки случая, когда станок не найден в БД (мокаем ошибку)."""
        mock_creator = MagicMock()
        mock_creator.by_name.return_value = None
        mock_container_class.return_value.creator.return_value = mock_creator

        self.assertIsNone(self.source.get_machine_tool("non_existent_model"))


class TestDefaultMachineToolSource(unittest.TestCase):
    """Тесты для класса DefaultMachineToolSource."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.source = DefaultMachineToolSource()

    def test_01_get_machine_tool_success(self):
        """Тест успешного получения данных о станке по умолчанию."""
        model_name = "DMG CTX beta 2000"
        result = self.source.get_machine_tool(model_name)

        self.assertIsInstance(result, MachineTool)
        self.assertEqual(result.model, model_name)
        self.assertEqual(result.length, Decimal("6234"))
        self.assertEqual(result.width, Decimal("3210"))
        self.assertEqual(result.height, Decimal("2052"))
        self.assertEqual(result.automation, "Автоматическая")
        self.assertEqual(result.weight, Decimal(10000.0))
        self.assertEqual(result.power_lathe_passport_kvt, Decimal(35.0))

    def test_02_get_machine_tool_not_supported(self):
        """Тест обработки неподдерживаемой модели."""
        with self.assertRaises(ValueError) as context:
            self.source.get_machine_tool("non_existent_model")
        self.assertEqual(str(context.exception), "Модель non_existent_model не поддерживается")


if __name__ == '__main__':
    unittest.main()
