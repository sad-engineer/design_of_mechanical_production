#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Optional, Union

from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel

from design_of_mechanical_production.gui.components.config import TableConfig
from design_of_mechanical_production.gui.components.interfaces import TableEventManager, TableRowFactory
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField


class EditableTable(FloatLayout):
    """
    Редактируемая таблица с прокруткой, рамкой и заголовком.
    """

    def __init__(
        self,
        config: TableConfig,
        row_factory: TableRowFactory,
        event_manager: Optional[TableEventManager] = None,
        height: float = 300,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.config = config
        self.row_factory = row_factory
        self.event_manager = event_manager
        self.table_rows = []
        self.height = height

        # Основной вертикальный layout (headers+scroll)
        self.vbox = BoxLayout(
            orientation='vertical', size_hint=(1, None), height=self.height, pos_hint={'x': 0, 'top': 0.91}
        )

        # Заголовки
        self.headers = GridLayout(
            cols=len(config.headers), size_hint=(1, None), height=40, spacing=2, padding=[0, 0, 0, 0]
        )
        for idx, header in enumerate(self.config.headers):
            label = MDLabel(text=header, bold=True, halign='center', size_hint_y=None, height=40)
            width = self.config.column_widths[idx]
            if width:
                label.size_hint_x = None
                label.width = width
            self.headers.add_widget(label)
        self.vbox.add_widget(self.headers)

        # Табличная часть (только строки)
        self.grid = GridLayout(cols=len(config.headers), size_hint_y=None, spacing=2, padding=[0, 0, 0, 0])
        self.grid.bind(minimum_height=self.grid.setter('height'))

        # Прокрутка
        self.scroll = ScrollView(
            size_hint=(1, None), height=self.height - 30
        )  # высота области прокрутки (можно менять)
        self.scroll.add_widget(self.grid)
        self.vbox.add_widget(self.scroll)
        self.add_widget(self.vbox)

        # Рамка вокруг vbox (headers+scroll), не затрагивает table_label
        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self._border = Line(rectangle=(0, 0, 0, 0), width=1.5)
        self.bind(pos=self._update_border, size=self._update_border)

    def _update_border(self, *args):
        """Обновляет рамку вокруг vbox (headers+scroll), не затрагивает table_label."""
        padding = 5
        x = self.vbox.x - padding
        y = self.vbox.y - padding
        w = self.vbox.width + 2 * padding
        h = self.vbox.height + 2 * padding
        self._border.rectangle = (x, y, w, h)

    def init(self):
        """Создает строки по данным в конфиге"""
        for row_data in self.config.initial_data:
            row_widgets = self.row_factory.create_row(row_data)
            self.event_manager.add_row(row_widgets)
        self.event_manager.add_empty_row()

    def add_widgets_to_layout(self, row_widgets: List[Any]):
        """Добавляет виджеты в контейнер таблицы."""
        for idx, widget in enumerate(row_widgets):
            width = self.config.column_widths[idx]
            if isinstance(widget, str):
                print(widget)
            if width:
                widget.size_hint_x = None
                widget.width = width
            self.grid.add_widget(widget)

    def get_data(self) -> list[dict[str, Union[Union[str, float], Any]]]:
        """Возвращает данные таблицы в виде списка словарей."""
        data = []
        for row in self.table_rows[:-1]:  # Пропускаем последнюю пустую строку
            row_data = []
            for widget in row:
                if hasattr(widget, 'text'):
                    row_data.append(widget.text)
                elif isinstance(widget, MachineToolSuggestField):
                    row_data.append(widget.text)
                else:
                    row_data.append('')
            data.append(row_data)

        process_data = []
        for row in data:
            process_data.append({'number': row[0], 'name': row[1], 'time': float(row[2]), 'machine': row[3]})
        return process_data

    def set_data(self, new_data: List[List[str]]):
        """Обновляет данные таблицы."""
        # Очищаем существующие строки
        for row in self.table_rows:
            for widget in row:
                self.grid.remove_widget(widget)
        self.table_rows = []
        # Добавляем новые строки
        for row_data in new_data:
            row_widgets = self.row_factory.create_row(row_data)
            self.event_manager.add_row(row_widgets)
        # Добавляем пустую строку
        self.event_manager.add_empty_row()
