#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List

from kivy.core.window import Window
from machine_tools import get_finder_with_list_names

from design_of_mechanical_production.gui.components.customized_spinner import CustomizedSpinner
from design_of_mechanical_production.gui.components.customized_text_input import CustomizedTextInput, TimeTextInput
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField
from design_of_mechanical_production.utils.machines import MACHINE_TOOL_OPERATION_MAP as OPERATION_MAP

machine_tool_finder = get_finder_with_list_names()


class TableRow:
    """
    Класс, представляющий строку таблицы.
    Содержит все виджеты строки и методы для работы с ними.
    """

    def __init__(self, row_data: List[str] = None, machine_name_replace: bool = True) -> None:
        row_data = row_data or [''] * 4

        # № Операция
        self.number_input = CustomizedTextInput(text=row_data[0])
        # Операция
        self.operation_spinner = CustomizedSpinner(
            text=row_data[1], items=OPERATION_MAP.keys(), on_item_selected=self._on_operation_selected
        )
        # Время
        self.time_input = TimeTextInput(text=row_data[2])
        # Станок
        self.machine_input = MachineToolSuggestField(row_data[3])
        Window.bind(mouse_pos=self._on_machine_mouse_pos)

        # Выбираем первую операцию
        if row_data[1]:
            self._on_operation_selected(row_data[1], machine_name_replace=machine_name_replace)

    def get_widgets(self) -> List[Any]:
        """Возвращает список всех виджетов строки."""
        return [self.number_input, self.operation_spinner, self.time_input, self.machine_input]

    def get_data(self) -> List[str]:
        """Возвращает данные строки в виде списка строк."""
        return [
            self.number_input.get_value(),
            self.operation_spinner.get_value(),
            self.time_input.get_value(),
            self.machine_input.get_value(),
        ]

    def set_data(self, data: List[str]) -> None:
        """Устанавливает данные строки."""
        self.number_input.set_value(data[0])
        self.operation_spinner.set_value(data[1])
        self.time_input.set_value(data[2])
        self.machine_input.set_value(data[3])

    def clear(self) -> None:
        """Очищает все поля строки."""
        self.number_input.clear_value()
        self.operation_spinner.clear_value()
        self.time_input.clear_value()
        self.machine_input.clear_value()

    def _on_machine_mouse_pos(self, instance, pos):
        """
        Обрабатывает движение мыши над полем ввода станка.

        Args:
            instance: Экземпляр Window
            pos: Позиция курсора
        """
        if self.machine_input.text_input.collide_point(*self.machine_input.text_input.to_widget(*pos)):
            self._validate_machine_name()
        else:
            self.machine_input.remove_tooltip()

    def _on_operation_selected(self, value: str, machine_name_replace: bool = True) -> None:
        """Функция вызывается при выборе операции в списке."""
        if value and value != "":
            machine_names = OPERATION_MAP[value]
            self.machine_input.machine_tools_names = machine_names
            machine = self.machine_input.text
            if machine not in machine_names and machine_name_replace:
                self.machine_input.text = machine_names[0]
            self._validate_machine_name()
        else:
            self.clear()
            self.machine_input.text = ""

    def _validate_machine_name(self) -> None:
        """Проверяет валидность введенного названия станка и управляет подсветкой и подсказкой."""
        operation = self.operation_spinner.text
        machine = self.machine_input.text

        self.machine_input.remove_tooltip()  # Сначала убираем подсказку

        if not machine:
            if operation:
                self.machine_input.set_style("error")
                self.machine_input.show_tooltip("Введите модель станка.")
            else:
                self.machine_input.set_style("normal")
        elif operation:
            machine_names = OPERATION_MAP[operation]
            if machine not in machine_names:
                self.machine_input.set_style("error")
                self.machine_input.show_tooltip("Станок не соответствует выбранной операции")
            else:
                self.machine_input.set_style("normal")
        else:
            self.machine_input.set_style("normal")

    def __del__(self):
        """Отвязываем обработчик события при удалении виджета."""
        Window.unbind(mouse_pos=self._on_machine_mouse_pos)
