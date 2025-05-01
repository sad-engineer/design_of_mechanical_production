#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List

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

    def __init__(self, config: TableConfig, row_factory: TableRowFactory, event_manager: TableEventManager, table_title: str = 'Название таблицы', height: float = 300, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.row_factory = row_factory
        self.event_manager = event_manager
        self.table_rows = []
        self.height = height

        # Заголовок таблицы (будет вне рамки)
        self.table_label = MDLabel(text=table_title, size_hint=(1, None), height=30, pos_hint={'top': 1, 'x': 0}, halign='center', font_style='H6')
        self.add_widget(self.table_label)

        # Основной вертикальный layout (headers+scroll)
        self.vbox = BoxLayout(orientation='vertical', size_hint=(1, None), height=self.height, pos_hint={'x': 0, 'top': 0.91})

        # Заголовки
        self.headers = GridLayout(cols=len(config.headers), size_hint=(1, None), height=40, spacing=2, padding=[0, 0, 0, 0])
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
        self.scroll = ScrollView(size_hint=(1, None), height=self.height - 30)  # высота области прокрутки (можно менять)
        self.scroll.add_widget(self.grid)
        self.vbox.add_widget(self.scroll)

        self.add_widget(self.vbox)

        # Рамка вокруг vbox (headers+scroll), не затрагивает table_label
        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self._border = Line(rectangle=(0, 0, 0, 0), width=1.5)
        self.bind(pos=self._update_border, size=self._update_border)

        # Инициализация строк
        self._init_rows()
        self.add_empty_row()

    def _update_border(self, *args):
        # Рамка только вокруг vbox (headers+scroll), не затрагивает table_label
        padding = 5
        x = self.vbox.x - padding
        y = self.vbox.y - padding
        w = self.vbox.width + 2 * padding
        h = self.vbox.height + 2 * padding
        self._border.rectangle = (x, y, w, h)

    def _init_rows(self):
        for row_data in self.config.initial_data:
            self._add_row(row_data)

    def _add_row(self, data: List[str] = None):
        row_widgets = self.row_factory.create_row(data)
        self._bind_row_events(row_widgets)
        self.table_rows.append(row_widgets)
        self._add_widgets_to_layout(row_widgets)

    def _bind_row_events(self, row_widgets: List[Any]):
        for widget in row_widgets:
            if isinstance(widget, TextInput):
                widget.bind(text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value))
            elif isinstance(widget, Spinner):
                widget.bind(text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value))
            elif isinstance(widget, MachineToolSuggestField):
                widget.text_input.bind(text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value))

    def _on_row_text_changed(self, row: List[Any], value: str):
        row_index = self.table_rows.index(row)
        row_data = [w.text if hasattr(w, 'text') else w.text_input.text if isinstance(w, MachineToolSuggestField) else '' for w in row]
        self.event_manager.on_row_changed(row_index, row_data)

    def _add_widgets_to_layout(self, row_widgets: List[Any]):
        for idx, widget in enumerate(row_widgets):
            width = self.config.column_widths[idx]
            if width:
                widget.size_hint_x = None
                widget.width = width
            self.grid.add_widget(widget)

    def add_empty_row(self):
        self._add_row()

    def get_data(self) -> List[List[str]]:
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
        return data

    def set_data(self, new_data: List[List[str]]):
        # Очищаем существующие строки
        for row in self.table_rows:
            for widget in row:
                self.grid.remove_widget(widget)
        self.table_rows = []
        # Добавляем новые строки
        for row_data in new_data:
            self._add_row(row_data)
        # Добавляем пустую строку
        self.add_empty_row()
