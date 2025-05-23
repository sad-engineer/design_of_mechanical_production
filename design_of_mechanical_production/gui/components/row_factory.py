#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List

from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from design_of_mechanical_production.gui.components.interfaces import TableRowFactory
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField
from design_of_mechanical_production.gui.components.spinner_option import MySpinnerOption
from design_of_mechanical_production.gui.components.time_input import TimeTextInput


class BaseTableRowFactory(TableRowFactory):
    """
    Базовая реализация фабрики строк таблицы.

    Attributes:
        operations: Список доступных операций.
    """

    def __init__(self, operations: List[str]):
        """
        Инициализирует фабрику строк.

        Args:
            operations: Список доступных операций.
        """
        self.operations = operations

    def create_row(self, data: List[str] = None) -> List[Any]:
        """
        Создает новую строку таблицы.

        Args:
            data: Данные для инициализации строки. Если None, создается пустая строка.

        Returns:
            List[Any]: Список виджетов строки.
        """
        data = data or [''] * 4
        row_widgets = []

        # №
        num_input = TextInput(text=data[0], multiline=False, size_hint_y=None, height=30, halign='center')
        row_widgets.append(num_input)

        # Операция
        operation_spinner = Spinner(
            text=data[1],
            values=self.operations,
            size_hint_y=None,
            height=30,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            option_cls=MySpinnerOption,
        )
        row_widgets.append(operation_spinner)

        # Время
        time_input = TimeTextInput(text=data[2], multiline=False, size_hint_y=None, height=30, halign='center')
        row_widgets.append(time_input)

        # Станок
        machine_input = MachineToolSuggestField(["16К20", "16К20Ф3"])
        if data[3]:
            machine_input.text = data[3]
        row_widgets.append(machine_input)

        return row_widgets
