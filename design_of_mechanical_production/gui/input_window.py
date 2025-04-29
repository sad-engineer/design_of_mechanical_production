#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.button import Button
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivy.uix.gridlayout import GridLayout
from typing import List, Dict, Any, Optional
from kivy.uix.dropdown import DropDown
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView

from machine_tools import MachineToolsContainer as Container

lister = Container().lister()
MACHINE_TOOLS = lister.all


class TimeTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        # Разрешаем ввод только цифр, запятой и точки (которая будет заменена на запятую)
        s = ''.join([c for c in substring if c.isdigit() or c in '.,'])
        # Заменяем точку на запятую
        s = s.replace('.', ',')
        return super().insert_text(s, from_undo=from_undo)

    def filter_text(self, text):
        # Разрешаем только одну запятую
        if text.count(',') > 1:
            return False
        return True


class EditableTable(GridLayout):
    """
    Универсальная таблица: только отрисовывает переданные заголовки и строки (список виджетов)
    """
    def __init__(self, headers: list, rows: list, col_widths: list = None, **kwargs):
        super().__init__(cols=len(headers), spacing=2, size_hint=(1, 1), padding=[0, 0, 0, 0], **kwargs)
        self.headers = headers
        self.table_rows = rows
        self.col_widths = col_widths or [None] * len(headers)

        # Заголовки
        for idx, header in enumerate(headers):
            label = MDLabel(
                text=header,
                bold=True,
                halign='center',
                size_hint_y=None,
                height=40
            )
            width = self.col_widths[idx]
            if width:
                label.size_hint_x = None
                label.width = width
            self.add_widget(label)

        # Строки
        for row in rows:
            for idx, widget in enumerate(row):
                width = self.col_widths[idx]
                if width:
                    widget.size_hint_x = None
                    widget.width = width
                self.add_widget(widget)

    def get_data(self):
        data = []
        for row in self.table_rows:
            row_data = []
            for widget in row:
                if hasattr(widget, 'text'):
                    row_data.append(widget.text)
                else:
                    row_data.append('')
            data.append(row_data)
        return data

    def set_data(self, new_data):
        for row_widgets, row_data in zip(self.table_rows, new_data):
            for widget, value in zip(row_widgets, row_data):
                if hasattr(widget, 'text'):
                    widget.text = str(value)


class MySpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 20


class MachineToolSuggestField(BoxLayout):
    def __init__(self, machine_tools, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=30, **kwargs)
        self.machine_tools = machine_tools
        self.text_input = TextInput(size_hint_y=None, height=30, multiline=False)
        self.text_input.bind(text=self.on_text)
        self.add_widget(self.text_input)
        self.suggestions_layout = None

    def on_text(self, instance, value):
        self.remove_suggestions()
        if len(value) >= 1:
            filtered = [tool for tool in self.machine_tools if value.lower() in tool.name.lower()]
            if filtered:
                max_rows = 5
                row_height = 30
                max_height = max_rows * row_height
                content_height = row_height * len(filtered)
                box = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=content_height
                )
                for tool in filtered:
                    btn = Button(text=tool.name, size_hint_y=None, height=row_height)
                    btn.bind(on_release=lambda btn, name=tool.name: self.select_tool(name))
                    box.add_widget(btn)
                scroll = ScrollView(
                    size_hint=(None, None),
                    size=(self.text_input.width, min(max_height, content_height)),
                    bar_width=8
                )
                scroll.add_widget(box)
                self.suggestions_layout = scroll
                x_win, y_win = self.text_input.to_window(self.text_input.x, self.text_input.y)
                self.suggestions_layout.pos = (x_win, y_win - self.suggestions_layout.height)
                Window.add_widget(self.suggestions_layout)

    def remove_suggestions(self):
        if self.suggestions_layout and self.suggestions_layout.parent:
            Window.remove_widget(self.suggestions_layout)
        self.suggestions_layout = None

    def select_tool(self, tool):
        self.text_input.text = tool
        self.remove_suggestions()

    @property
    def text(self):
        return self.text_input.text

    @text.setter
    def text(self, value):
        self.text_input.text = value


class InputWindow(FloatLayout):
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager

        # Создаем однострочный контейнер для иконок
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),  # Отключаем растягивание
            width=50,  # Минимальная ширина для двух иконок
            height=40,
            padding=0,
            spacing=0,
            pos=(Window.width - 100, Window.height - 50)  # Отступ справа и сверху
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
            size_hint=(1, None),  # Растягиваем по ширине
            height=50,
            pos=(0, Window.height - 50),  # Центрируем по ширине
            halign='center',
            font_style='H5'
        )
        self.add_widget(self.label)

        # --- Два столбца ---
        columns = BoxLayout(
            orientation='horizontal',
            size_hint=(1.2, 1),
            spacing=0,
            padding=0
        )

        # Левый столбец (настройки параметров)
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
        left_col.add_widget(MDLabel(text='Годовой объем производства (шт.):', halign='left', size_hint_y=None, height=30))
        self.volume_input = TextInput(text='10000', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.volume_input)
        # Масса детали
        left_col.add_widget(MDLabel(text='Масса детали (кг):', halign='left', size_hint_y=None, height=30))
        self.mass_input = TextInput(text='112.8', size_hint_y=None, halign='center', height=30)
        left_col.add_widget(self.mass_input)
        columns.add_widget(left_col)

        # Правая часть (редактируемая таблица в FloatLayout)
        right_col = FloatLayout(size_hint_x=None, width=600)

        # --- Редактируемая таблица ---
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

        # Конфигурация таблицы
        headers = ["№", "Операция", "Время", "Станок"]
        col_widths = [40, 175, 80, None]
        initial_data = [
            ["005", "Токарная с ЧПУ", "11.67", "DMG CTX beta 2000"],
            ["010", "Расточная с ЧПУ", "20.82", "2431СФ10"],
            ["015", "Токарная с ЧПУ", "5.65", "DMG CTX beta 2000"],
            ["020", "Фрезерная с ЧПУ", "1.86", "DMU 50"]
        ]

        # Формируем виджеты для таблицы
        rows = []
        for row in initial_data:
            row_widgets = []
            # №
            row_widgets.append(TextInput(text=row[0], multiline=False, size_hint_y=None, height=30, halign='center'))
            # Операция
            row_widgets.append(Spinner(text=row[1], values=self.operations, size_hint_y=None, height=30, background_normal='', background_color=(0.9, 0.9, 0.9, 1), option_cls=MySpinnerOption))
            # Время
            row_widgets.append(TimeTextInput(text=str(row[2]).replace('.', ','), multiline=False, size_hint_y=None, height=30, halign='center'))
            # Станок
            row_widgets.append(MachineToolSuggestField(MACHINE_TOOLS))
            rows.append(row_widgets)
        self.table = EditableTable(headers=headers, rows=rows, col_widths=col_widths)
        self.table.size_hint = (1, None)
        self.table.height = right_col.height
        self.table.pos_hint = {'x': 0, 'y': 0}
        right_col.add_widget(self.table)
        right_col.bind(height=lambda instance, value: setattr(self.table, 'height', value))
        columns.add_widget(right_col)

        self.add_widget(columns)

        # Привязываем обработчик изменения размера окна
        Window.bind(size=self.update_positions)

    def update_positions(self, instance, size):
        width, height = size
        self.header.pos = (width - 100, height - 50)
        self.label.pos = (0, height - 50)

    def save_data(self, instance):
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
    
    def cancel(self, instance):
        # Здесь можно добавить закрытие окна
        print("Отмена ввода")

    def toggle_theme(self, instance):
        app = MDApp.get_running_app()
        if app.theme_cls.theme_style == "Light":
            app.theme_cls.theme_style = "Dark"
        else:
            app.theme_cls.theme_style = "Light"

    def open_settings(self, instance):
        if self.screen_manager:
            self.screen_manager.current = 'settings'
        else:
            print("screen_manager не передан!")

    def get_table_data(self):
        """Получить все данные из таблицы"""
        return self.table.get_data()

    def set_table_data(self, new_data):
        """Обновить данные в таблице"""
        self.table.set_data(new_data)


class InputApp(App):
    def build(self):
        Window.size = (400, 300)
        return InputWindow()


if __name__ == '__main__':
    InputApp().run()
