#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Any

from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from design_of_mechanical_production.gui.components.interfaces import TableEventManager
from design_of_mechanical_production.gui.components.table import EditableTable
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField


class TableEventManagerImpl(TableEventManager):
    """
    Реализация менеджера событий таблицы.

    Attributes:
        table: Экземпляр таблицы, для которой обрабатываются события.
    """

    def __init__(self, table: EditableTable):
        """
        Инициализирует менеджер событий.

        Args:
            table: Экземпляр таблицы, для которой обрабатываются события.
        """
        self.table = table

    def add_row(self, row_widgets: List[Any]):
        """Добавляет строку в таблицу."""
        # Получаем виджеты из фабрики
        self.table.table_rows.append(row_widgets)
        # Устнавливаем связи новых виджетов с событиями таблицы
        self.bind_row_events(row_widgets)
        # Усданавливаем новые виджеты в контейнер таблицы
        self.table.add_widgets_to_layout(row_widgets)

    def add_empty_row(self):
        """Добавляет пустую строку в таблицу."""
        row_widgets = self.table.row_factory.create_row()
        if self.table.table_rows[-1][0].text or self.table.table_rows[-1][2].text or self.table.table_rows[-1][3].text:
            self.add_row(row_widgets)
    
    def remove_row(self, row_index: int):
        """Удаляет строку из таблицы."""
        for widget in self.table.table_rows[row_index]:
            if isinstance(widget, MachineToolSuggestField):
                widget.remove_suggestions()
            self.table.grid.remove_widget(widget)
        del self.table.table_rows[row_index]

    def bind_row_events(self, row_widgets: List[Any]):
        """
        Связывает события с строками.

        Args:
            row_widgets: Список виджетов строки.
        """
        for widget in row_widgets:
            if isinstance(widget, TextInput):
                widget.bind(text=lambda instance, value, row=row_widgets: self.on_row_text_changed(row, value))
            elif isinstance(widget, Spinner):
                widget.bind(text=lambda instance, value, row=row_widgets: self.on_row_text_changed(row, value))
            elif isinstance(widget, MachineToolSuggestField):
                widget.text_input.bind(
                    text=lambda instance, value, row=row_widgets: self.on_row_text_changed(row, value)
                )

    def on_row_text_changed(self, row: List[Any], value: str):
        """
        Обрабатывает изменения в строке.

        Args:
            row: Список виджетов измененной строки.
            value: Новое значение.
        """
        row_index = self.table.table_rows.index(row)
        row_data = [
            w.text if hasattr(w, 'text') else w.text_input.text if isinstance(w, MachineToolSuggestField) else ''
            for w in row
        ]
        self.on_row_changed(row_index, row_data)
        self.add_empty_row()

    def on_row_changed(self, row_index: int, data: List[str]):
        """
        Обрабатывает изменение строки.

        Args:
            row_index: Индекс измененной строки.
            data: Новые данные строки.
        """

        if row_index == len(self.table.table_rows) - 1 and any(data):
            self.add_empty_row()
        if all([data[0] == "", data[2] == "", data[3] == ""]):
            self.remove_row(row_index)
    

