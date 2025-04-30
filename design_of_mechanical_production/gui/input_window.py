#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит основной класс окна ввода данных.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

from design_of_mechanical_production.gui.components.config import TableConfig
from design_of_mechanical_production.gui.components.row_factory import BaseTableRowFactory
from design_of_mechanical_production.gui.components.event_manager import TableEventManagerImpl
from design_of_mechanical_production.gui.components.table import EditableTable


class InputWindow(FloatLayout):
    """
    Окно ввода данных.

    Attributes:
        screen_manager: Менеджер экранов приложения.
        operations: Список доступных операций.
        table: Таблица с данными.
    """
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self._init_operations()
        self._init_ui()

    def _init_operations(self):
        """Инициализирует список доступных операций."""
        self.operations = [
            "Токарная",
            "Токарная с ЧПУ",
            "Сверлильная",
            "Сверлильная с ЧПУ",
            "Расточная",
            "Расточная с ЧПУ",
            "Фрезерная",
            "Фрезерная с ЧПУ",
            "Шлифовальная",
            "Шлифовальная с ЧПУ",
        ]

    def _init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        self._create_header()
        self._create_columns()

        # Программно изменяем размер окна для пересчета позиций
        def trigger_resize(dt):
            current_width = Window.width
            current_height = Window.height
            Window.size = (current_width + 1, current_height + 1)
            Clock.schedule_once(lambda dt: setattr(Window, 'size', (current_width, current_height)), 0.1)

        Clock.schedule_once(trigger_resize, 0)

    def _create_header(self):
        """Создает заголовок окна."""
        # Создаем однострочный контейнер для иконок
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            width=50,
            height=40,
            padding=0,
            spacing=0,
            pos=(Window.width - 100, Window.height - 50)
        )

        # Добавляем иконки
        self.theme_btn = MDIconButton(
            icon="theme-light-dark",
            size_hint=(None, None),
            size=(40, 40),
            padding=0,
            on_release=self.toggle_theme
        )
        self.header.add_widget(self.theme_btn)

        self.settings_btn = MDIconButton(
            icon="cog",
            size_hint=(None, None),
            size=(40, 40),
            padding=0,
            on_release=self.open_settings
        )
        self.header.add_widget(self.settings_btn)

        self.add_widget(self.header)

        # Добавляем заголовок
        self.label = MDLabel(
            text='Ввод начальных условий',
            size_hint=(1, None),
            height=50,
            pos=(0, Window.height - 50),
            halign='center',
            font_style='H5'
        )
        self.add_widget(self.label)

    def _create_columns(self):
        """Создает основные колонки интерфейса."""
        columns = BoxLayout(orientation='horizontal', size_hint=(1.2, 1), spacing=0, padding=0)

        # Левый столбец
        left_col = self._create_left_column()
        columns.add_widget(left_col)

        # Правая часть с таблицей
        right_col = self._create_table_column()
        columns.add_widget(right_col)

        self.add_widget(columns)

    def _create_left_column(self):
        """Создает левую колонку с настройками."""
        left_col = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            width=300,
            padding=[20, 10, 10, 10],
            spacing=10
        )

        # Название цеха
        left_col.add_widget(MDLabel(text='Название цеха:', halign='left', size_hint_y=None, height=30))
        self.name_input = TextInput(text='Механический цех №1', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.name_input)

        # Годовой объем производства
        left_col.add_widget(
            MDLabel(text='Годовой объем производства (шт.):', halign='left', size_hint_y=None, height=30))
        self.volume_input = TextInput(text='10000', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.volume_input)

        # Масса детали
        left_col.add_widget(MDLabel(text='Масса детали (кг):', halign='left', size_hint_y=None, height=30))
        self.mass_input = TextInput(text='112.8', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.mass_input)

        return left_col

    def _create_table_column(self):
        """Создает правую колонку с таблицей."""
        right_col = FloatLayout(size_hint_x=None, width=600)

        # Создаем конфигурацию таблицы
        table_config = TableConfig(
            headers=["№", "Операция", "Время", "Станок"],
            column_widths=[40, 175, 80, None],
            initial_data=[
                ["005", "Токарная с ЧПУ", "11.67", "DMG CTX beta 2000"],
                ["010", "Расточная с ЧПУ", "20.82", "2431СФ10"],
                ["015", "Токарная с ЧПУ", "5.65", "DMG CTX beta 2000"],
                ["020", "Фрезерная с ЧПУ", "1.86", "DMU 50"]
            ],
            operations=self.operations
        )

        # Создаем фабрику строк
        row_factory = BaseTableRowFactory(self.operations)

        # Создаем таблицу
        self.table = EditableTable(
            config=table_config,
            row_factory=row_factory,
            event_manager=None
        )
        self.table.size_hint = (1, None)
        self.table.bind(minimum_height=self.table.setter('height'))

        # Создаем и устанавливаем менеджер событий
        self.table.event_manager = TableEventManagerImpl(self.table)

        # Создаем ScrollView для таблицы
        scroll_view = ScrollView(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0},
            bar_width=10,
            bar_color=(0.5, 0.5, 0.5, 1),
            bar_inactive_color=(0.7, 0.7, 0.7, 1),
            scroll_type=['bars', 'content']
        )
        scroll_view.add_widget(self.table)
        right_col.add_widget(scroll_view)

        return right_col

    def save_data(self, instance):
        """Сохраняет введенные данные."""
        try:
            data = {
                'name': [self.name_input.text],
                'production_volume': [int(self.volume_input.text)],
                'mass_detail': [float(self.mass_input.text)]
            }
            # Здесь можно добавить сохранение данных
            print("Данные сохранены:", data)
        except ValueError as e:
            print("Ошибка ввода данных:", e)

    @staticmethod
    def cancel(instance):
        """Отменяет ввод данных."""
        print("Отмена ввода")

    @staticmethod
    def toggle_theme(instance):
        """Переключает тему приложения."""
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"

    def open_settings(self, instance):
        """Открывает окно настроек."""
        if self.screen_manager:
            self.screen_manager.current = 'settings'
        else:
            print("screen_manager не передан!")

    def get_table_data(self):
        """Возвращает данные из таблицы."""
        return self.table.get_data()

    def set_table_data(self, new_data):
        """Устанавливает новые данные в таблицу."""
        self.table.set_data(new_data)
