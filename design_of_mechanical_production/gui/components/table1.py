#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, Dict, List, Union
from kivy.app import App
from kivy.graphics import Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp

from design_of_mechanical_production.gui.components.config import TableConfig
from design_of_mechanical_production.gui.components.interfaces import TableEventManager, TableRowFactory
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField
from design_of_mechanical_production.data.input import ExcelReader

from design_of_mechanical_production.settings import get_setting
from pathlib import Path


class EditableTable(FloatLayout):
    """
    Редактируемая таблица с прокруткой, рамкой и заголовком.
    """
    def __init__(
        self,
        config: TableConfig,
        row_factory: TableRowFactory,
        event_manager: TableEventManager,
        table_title: str = 'Название таблицы',
        height: float = 300,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.config = config
        self.row_factory = row_factory
        self.event_manager = event_manager
        self.table_rows = []
        self.height = height

        # Заголовок таблицы (будет вне рамки)
        self.table_label = MDLabel(
            text=table_title,
            size_hint=(1, None),
            height=30,
            pos_hint={'top': 1, 'x': 0},
            halign='center',
            font_style='H6',
        )
        self.add_widget(self.table_label)

        # Основной вертикальный layout (headers+scroll)
        self.vbox = BoxLayout(
            orientation='vertical', size_hint=(1, None), height=self.height, pos_hint={'x': 0, 'top': 0.91}
        )

        # Заголовки
        self.headers = GridLayout(
            cols=len(config.headers) + 1,  # +1 для кнопки удаления
            size_hint=(1, None), height=40, spacing=2, padding=[0, 0, 0, 0]
        )
        for idx, header in enumerate(self.config.headers):
            label = MDLabel(text=header, bold=True, halign='center', size_hint_y=None, height=40)
            width = self.config.column_widths[idx]
            if width:
                label.size_hint_x = None
                label.width = width
            self.headers.add_widget(label)
        # Добавляем пустой заголовок для кнопки удаления
        delete_header = MDLabel(text="", size_hint_y=None, width=40, height=40)
        self.headers.add_widget(delete_header)
        self.vbox.add_widget(self.headers)

        # Табличная часть (только строки)
        self.grid = GridLayout(
            cols=len(config.headers) + 1,  # +1 для кнопки удаления
            size_hint_y=None, spacing=2, padding=[0, 0, 0, 0]
        )
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
        # Привязываем обработчик к кнопке удаления (последний виджет)
        delete_btn = row_widgets[-1]
        delete_btn.bind(on_release=lambda instance: self._delete_row(row_widgets))
        self.table_rows.append(row_widgets)
        self._add_widgets_to_layout(row_widgets)

    def _bind_row_events(self, row_widgets: List[Any]):
        for widget in row_widgets:
            if isinstance(widget, TextInput):
                widget.bind(text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value))
            elif isinstance(widget, Spinner):
                widget.bind(text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value))
            elif isinstance(widget, MachineToolSuggestField):
                widget.text_input.bind(
                    text=lambda instance, value, row=row_widgets: self._on_row_text_changed(row, value)
                )

    def _on_row_text_changed(self, row: List[Any], value: str):
        row_index = self.table_rows.index(row)
        row_data = [
            w.text if hasattr(w, 'text') else w.text_input.text if isinstance(w, MachineToolSuggestField) else ''
            for w in row
        ]
        self.event_manager.on_row_changed(row_index, row_data)
        self.clean_empty_rows()

    def clean_empty_rows(self):
        """Оставляет только одну пустую строку в конце таблицы."""
        # Считаем пустые строки (все поля пустые)
        empty_rows = []
        for idx, row in enumerate(self.table_rows):
            if all(
                (getattr(w, 'text', '') == '' if not isinstance(w, MachineToolSuggestField) else w.text == '')
                for w in row
            ):
                empty_rows.append(idx)
        # Если пустых строк больше одной, удаляем все кроме последней
        if len(empty_rows) > 1:
            # Удаляем с конца, чтобы индексы не сбивались
            for idx in reversed(empty_rows[:-1]):
                for widget in self.table_rows[idx]:
                    self.grid.remove_widget(widget)
                del self.table_rows[idx]

    def _add_widgets_to_layout(self, row_widgets: List[Any]):
        for idx, widget in enumerate(row_widgets):
            # Если это последняя ячейка (кнопка удаления)
            if idx == len(row_widgets) - 1:
                widget.size_hint_x = None
                widget.width = 40
            else:
                width = self.config.column_widths[idx]
                if width:
                    widget.size_hint_x = None
                    widget.width = width
            self.grid.add_widget(widget)

    def _delete_row(self, row_widgets: List[Any]):
        """Удаляет строку из таблицы."""
        if len(self.table_rows) > 1:  # Не удаляем, если это последняя строка
            row_index = self.table_rows.index(row_widgets)
            # Удаляем все виджеты строки
            for widget in row_widgets:
                self.grid.remove_widget(widget)
            # Удаляем кнопку удаления
            self.grid.remove_widget(self.grid.children[0])
            # Удаляем строку из списка
            del self.table_rows[row_index]
            # Уведомляем о изменении
            self.event_manager.on_row_changed(row_index, None)
            # Проверяем, осталась ли пустая строка в конце, если нет — добавляем
            if not self._has_empty_row():
                self.add_empty_row()

    def _has_empty_row(self):
        """Проверяет, есть ли пустая строка в конце таблицы."""
        if not self.table_rows:
            return False
        last_row = self.table_rows[-1]
        # Не учитываем кнопку удаления
        for w in last_row[:-1]:
            if hasattr(w, 'text') and w.text.strip():
                return False
            if isinstance(w, MachineToolSuggestField) and w.text.strip():
                return False
        return True

    def add_empty_row(self):
        self._add_row()

    def get_data(self) -> list[dict[str, Union[Union[str, float], Any]]]:
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
            if len(row) >= 4:
                process_data.append({'number': row[0], 'name': row[1], 'time': float(row[2]), 'machine': row[3]})
        return process_data

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


if __name__ == "__main__":
    class DummyEventManager:
        def on_row_changed(self, row_index, row_data):
            print(f"Row {row_index} changed: {row_data}")

    class DummyRowFactory:
        def __init__(self, operations, delete_callback=None):
            self.operations = operations
            self.delete_callback = delete_callback  # Сохраняем колбэк для удаления

        def create_row(self, data=None):
            from kivy.uix.textinput import TextInput
            from kivy.uix.spinner import Spinner
            if data is None:
                data = ["", "", "", ""]
            row_widgets = [
                TextInput(text=data[0]),
                Spinner(text=data[1], values=self.operations),
                TextInput(text=data[2]),
                TextInput(text=data[3]),
            ]
            # Кнопка удаления
            delete_btn = MDIconButton(
                icon='delete',
                size_hint=(None, None),
                size=(30, 30),
                pos_hint={'center_y': 0.5},
            )
            row_widgets.append(delete_btn)
            return row_widgets

    class TestTableApp(MDApp):
        def build(self):
            reader = ExcelReader(Path(get_setting('input_data_path')))
            process_data = reader.read_process_data()
            process = [[str(d['number']), d['name'], str(d['time']), str(d['machine'])] for d in process_data]

            operations = ["Операция 1", "Операция 2", "Операция 3"]
            config = TableConfig(
                headers=["№", "Операция", "Время", "Станок"],
                column_widths=[40, 175, 80, None],
                initial_data=process,
                operations=operations,
            )
            table = EditableTable(
                config=config,
                row_factory=DummyRowFactory(operations),
                event_manager=DummyEventManager(),
                table_title="Тестовая таблица",
                height=300,
            )
            root = BoxLayout(orientation='vertical')
            root.add_widget(table)
            return root

    TestTableApp().run()
