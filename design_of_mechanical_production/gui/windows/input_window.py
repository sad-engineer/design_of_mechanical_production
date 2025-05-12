#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна ввода данных, наследующий от шаблонного окна.
"""
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from design_of_mechanical_production.core.services.workshop_creator import create_workshop_from_data
from design_of_mechanical_production.gui.components.config import TableConfig
from design_of_mechanical_production.gui.components.event_manager import TableEventManagerImpl
from design_of_mechanical_production.gui.components.row_factory import BaseTableRowFactory
from design_of_mechanical_production.gui.components.table import EditableTable
from design_of_mechanical_production.gui.windows.template_window import TemplateWindow

OPERATIONS = [
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


class TemplateInputWindow(TemplateWindow):
    """
    Окно ввода данных, наследующее от шаблонного окна.

    Attributes:
        operations: Список доступных операций.
        table: Таблица с данными.
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)
        # Инициализируем наш контент
        self._init_content()
        # Инициализируем кнопки
        self._init_buttons()

    def _init_content(self):
        """Инициализирует содержимое окна."""
        columns = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=1,
        )
        left_col = self._create_left_column()
        right_col = self._create_table_column()
        columns.add_widget(left_col)
        columns.add_widget(right_col)
        self.content.add_widget(columns)

    def _create_left_column(self):
        """Создает левую колонку с настройками."""
        left_col = BoxLayout(
            orientation='vertical',
            width=275,
            size_hint_x=None,
        )

        # Название цеха
        left_col.add_widget(MDLabel(text='Название цеха:', halign='left', size_hint_y=None, height=30))
        self.name_input = TextInput(text='Механический цех №1', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.name_input)

        # Годовой объем производства
        left_col.add_widget(
            MDLabel(text='Годовой объем производства (шт.):', halign='left', size_hint_y=None, height=30)
        )
        self.volume_input = TextInput(text='10000', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.volume_input)

        # Масса детали
        left_col.add_widget(MDLabel(text='Масса детали (кг):', halign='left', size_hint_y=None, height=30))
        self.mass_input = TextInput(text='112.8', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.mass_input)

        left_col.add_widget(Widget(size_hint_y=1))

        left_col.bind(pos=self._update_left_col_debug, size=self._update_left_col_debug)
        return left_col

    def _create_table_column(self):
        """Создает правую колонку с таблицей."""
        right_col = BoxLayout(height=400, width=275, orientation='vertical')

        # Создаем конфигурацию таблицы
        table_config = TableConfig(
            headers=["№", "Операция", "Время", "Станок"],
            column_widths=[40, 175, 80, None],
            initial_data=[
                ["005", "Токарная с ЧПУ", "11.67", "DMG CTX beta 2000"],
                ["010", "Расточная с ЧПУ", "20.82", "2431СФ10"],
                ["015", "Токарная с ЧПУ", "5.65", "DMG CTX beta 2000"],
                ["020", "Фрезерная с ЧПУ", "1.86", "DMU 50"],
            ],
            operations=OPERATIONS,
        )

        # Создаем фабрику строк
        row_factory = BaseTableRowFactory(OPERATIONS)

        # Создаем таблицу (теперь она сама содержит прокрутку и рамку)
        self.table = EditableTable(
            config=table_config,
            row_factory=row_factory,
            event_manager=None,
            pos_hint={'x': 0, 'top': 1},
            size_hint=(1, 1),
            height=400,
            table_title='Технологический процесс изготовления детали',
        )
        self.table.event_manager = TableEventManagerImpl(self.table)
        right_col.add_widget(self.table)

        right_col.bind(pos=self._update_right_col_debug, size=self._update_right_col_debug)
        return right_col

    def _update_left_col_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 0, 0.3)  # Черный с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    def _update_right_col_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 1, 0.3)  # Синий с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    def _init_buttons(self):
        """Инициализирует кнопки управления."""
        # Очищаем существующие кнопки
        self.buttons_box.clear_widgets()

        # Создаем новые кнопки
        calc_btn = Button(
            text='Начать расчет', size_hint=(None, 1), width=self.max_button_width, on_release=self.save_data
        )
        cancel_btn = Button(text='Отмена', size_hint=(None, 1), width=self.max_button_width, on_release=self.cancel)

        # Добавляем кнопки в контейнер
        self.buttons_box.add_widget(calc_btn)
        self.buttons_box.add_widget(cancel_btn)

    def save_data(self, instance):
        """Сохраняет введенные данные и переходит к результатам расчета."""
        try:
            # Получаем данные параметров
            parameters_data = {
                'name': self.name_input.text,
                'production_volume': int(self.volume_input.text),
                'mass_detail': float(self.mass_input.text),
            }
            # Получаем данные из таблицы и преобразуем их в нужный формат
            process_data = self.table.get_data()
            # Делаем расчет
            workshop = create_workshop_from_data(parameters_data, process_data)

            # Переходим к окну результатов
            if self.screen_manager:
                # Передаем workshop в окно результатов
                result_screen = self.screen_manager.get_screen('result_window')
                result_screen.set_workshop(workshop)
                self.screen_manager.current = 'result_window'
            else:
                print("Ошибка: screen_manager не передан!")

        except ValueError as e:
            print("Ошибка ввода данных:", e)

    def get_table_data(self):
        """Возвращает данные из таблицы."""
        return self.table.get_data()

    def set_table_data(self, new_data):
        """Устанавливает новые данные в таблицу."""
        self.table.set_data(new_data)


class InputWindow(Screen):
    """Окно ввода данных, обертка для TemplateInputWindow."""

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = 'input_window'
        # Создаем и добавляем TemplateInputWindow
        self.template_window = TemplateInputWindow(screen_manager=screen_manager, debug_mode=debug_mode)
        self.add_widget(self.template_window)

    def get_table_data(self):
        """Возвращает данные из таблицы."""
        return self.template_window.get_table_data()

    def set_table_data(self, new_data):
        """Устанавливает новые данные в таблицу."""
        self.template_window.set_table_data(new_data)


if __name__ == '__main__':

    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            Window.minimum_width = 910
            Window.minimum_height = 500
            window = InputWindow(debug_mode=True)
            return window

    TestApp().run()
