#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Any
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

from design_of_mechanical_production.gui.components.interfaces import TableRowFactory, TableEventManager
from design_of_mechanical_production.gui.components.config import TableConfig
from design_of_mechanical_production.gui.components.machine_tool_suggest_field import MachineToolSuggestField


class EditableTable(GridLayout):
    """
    Редактируемая таблица.
    
    Attributes:
        config: Конфигурация таблицы.
        row_factory: Фабрика для создания строк.
        event_manager: Менеджер событий таблицы.
        table_rows: Список строк таблицы.
    """
    
    def __init__(self, config: TableConfig, row_factory: TableRowFactory, event_manager: TableEventManager, **kwargs):
        """
        Инициализирует таблицу.
        
        Args:
            config: Конфигурация таблицы.
            row_factory: Фабрика для создания строк.
            event_manager: Менеджер событий таблицы.
            **kwargs: Дополнительные аргументы для GridLayout.
        """
        super().__init__(cols=len(config.headers), spacing=2, size_hint=(1, 1), padding=[0, 0, 0, 0], **kwargs)
        self.config = config
        self.row_factory = row_factory
        self.event_manager = event_manager
        self.table_rows = []
        
        self._init_headers()
        self._init_rows()
        self.add_empty_row()

    def _init_headers(self):
        """Инициализирует заголовки таблицы."""
        for idx, header in enumerate(self.config.headers):
            label = MDLabel(
                text=header,
                bold=True,
                halign='center',
                size_hint_y=None,
                height=40
            )
            width = self.config.column_widths[idx]
            if width:
                label.size_hint_x = None
                label.width = width
            self.add_widget(label)

    def _init_rows(self):
        """Инициализирует начальные строки таблицы."""
        for row_data in self.config.initial_data:
            self._add_row(row_data)

    def _add_row(self, data: List[str] = None):
        """
        Добавляет новую строку в таблицу.
        
        Args:
            data: Данные для инициализации строки. Если None, создается пустая строка.
        """
        row_widgets = self.row_factory.create_row(data)
        self._bind_row_events(row_widgets)
        self.table_rows.append(row_widgets)
        self._add_widgets_to_layout(row_widgets)

    def _bind_row_events(self, row_widgets: List[Any]):
        """
        Привязывает обработчики событий к виджетам строки.
        
        Args:
            row_widgets: Список виджетов строки.
        """
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
        """
        Обрабатывает изменение текста в строке.
        
        Args:
            row: Список виджетов строки
            value: Новое значение
        """
        row_index = self.table_rows.index(row)
        row_data = [w.text if hasattr(w, 'text') else w.text_input.text if isinstance(
            w, MachineToolSuggestField
        ) else '' for w in row]
        self.event_manager.on_row_changed(row_index, row_data)

    def _add_widgets_to_layout(self, row_widgets: List[Any]):
        """
        Добавляет виджеты строки в layout.
        
        Args:
            row_widgets: Список виджетов строки.
        """
        for idx, widget in enumerate(row_widgets):
            width = self.config.column_widths[idx]
            if width:
                widget.size_hint_x = None
                widget.width = width
            self.add_widget(widget)

    def add_empty_row(self):
        """Добавляет пустую строку в конец таблицы."""
        self._add_row()

    def get_data(self) -> List[List[str]]:
        """
        Возвращает данные таблицы.
        
        Returns:
            List[List[str]]: Список строк с данными.
        """
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
        """
        Устанавливает новые данные в таблицу.
        
        Args:
            new_data: Новые данные таблицы.
        """
        # Очищаем существующие строки
        for row in self.table_rows:
            for widget in row:
                self.remove_widget(widget)
        self.table_rows = []
        
        # Добавляем новые строки
        for row_data in new_data:
            self._add_row(row_data)
        
        # Добавляем пустую строку
        self.add_empty_row()
