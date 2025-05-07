#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна отображения результатов расчета.
"""
from pathlib import Path

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from design_of_mechanical_production.core import create_workshop_from_data
from design_of_mechanical_production.data.input import ExcelReader
from design_of_mechanical_production.data.output import TextReportGenerator
from design_of_mechanical_production.data.output.formatters import NumberFormatter
from design_of_mechanical_production.data.utils.file_system import (
    create_initial_data_file,
)
from design_of_mechanical_production.gui.windows.template_window import TemplateWindow
from design_of_mechanical_production.settings import get_setting

number_formatter = NumberFormatter()
fn = number_formatter.format


class TemplateResultWindow(TemplateWindow):
    """
    Окно отображения результатов расчета.

    Attributes:
        screen_manager: Менеджер экранов приложения
        workshop: Объект цеха с результатами расчета
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)

        self.screen_manager = screen_manager
        self._workshop = None
        # создаем  контент
        self._create_content()
        # Инициализируем кнопки
        self._init_buttons()

    def _create_content(self):
        """Создает основной контент с результатами."""
        # Создаем ScrollView для прокрутки контента
        scroll_view = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            do_scroll_x=False,
        )
        # Создаем контейнер для карточек с результатами
        self.content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10,
        )
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        self.content_layout.bind(pos=self._update_content_debug, size=self._update_content_debug)
        scroll_view.add_widget(self.content_layout)
        self.content.add_widget(scroll_view)

    def _init_buttons(self):
        """Инициализирует кнопки управления."""
        # Очищаем существующие кнопки
        self.buttons_box.clear_widgets()

        # Создаем новые кнопки
        back_to_input = Button(
            text='Назад', size_hint=(None, 1), width=self.max_button_width, on_release=self.back_to_input
        )
        export_results = Button(
            text='Экспорт', size_hint=(None, 1), width=self.max_button_width, on_release=self.export_results
        )

        # Добавляем кнопки в контейнер
        self.buttons_box.add_widget(back_to_input)
        self.buttons_box.add_widget(export_results)

    def back_to_input(self, instance):
        """
        Возвращает к окну ввода данных.
        """
        if self.screen_manager:
            self.workshop = None
            self.content.clear_widgets()
            self.screen_manager.current = 'input_window'

    def export_results(self, instance):
        """
        Экспортирует результаты расчета в текстовый отчет.
        """
        if not self.workshop:
            print("Нет данных для экспорта")
            return

        try:
            # Генерация и сохранение отчета
            report_generator = TextReportGenerator()
            report = report_generator.generate_report(self.workshop)

            report_path = Path(get_setting('report_path'))
            if report_generator.save_report(report, report_path):
                print(f"Отчет успешно сгенерирован и сохранен в {report_path}")
            else:
                print("Ошибка при сохранении отчета")

        except Exception as e:
            print(f"Ошибка при экспорте результатов: {e}")

    def _update_content_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 1, 0.5)  # белый с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    @property
    def workshop(self):
        return self._workshop

    @workshop.setter
    def workshop(self, workshop):
        """
        Устанавливает объект цеха и обновляет отображение.

        Args:
            workshop: Объект цеха с результатами расчета.
        """
        self._workshop = workshop
        if self._workshop:
            self._update_content()

    def _update_content(self):
        """Обновляет отображение результатов расчета."""

        # Очищаем предыдущий контент
        self.content_layout.clear_widgets()

        # Создаем карточки с результатами
        self._add_general_info_card()
        self._add_process_info_card()
        self._add_zones_info_card()

    def _add_general_info_card(self):
        """Добавляет карточку с общей информацией о цехе."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=150,
            padding=15,
            spacing=10,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Исходные данные',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация
        info_layout = BoxLayout(orientation='vertical', spacing=5)
        info_layout.add_widget(MDLabel(text=f'Название цеха: {self.workshop.name}'))
        info_layout.add_widget(MDLabel(text=f'Годовой объем производства: {self.workshop.production_volume} шт.'))
        info_layout.add_widget(MDLabel(text=f'Масса детали: {fn(self.workshop.mass_detail)} кг'))
        info_layout.add_widget(MDLabel(text=f'Общая площадь цеха: {fn(self.workshop.total_area)} м²'))

        card.add_widget(info_layout)
        self.content_layout.add_widget(card)

    def _add_process_info_card(self):
        """Добавляет карточку с информацией о технологическом процессе."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=200,
            padding=15,
            spacing=10,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Технологический процесс',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация о процессе
        process_layout = BoxLayout(orientation='vertical', spacing=5)
        for operation in self.workshop.process.operations:
            process_layout.add_widget(
                MDLabel(
                    text=f'Операция {operation.number}: {operation.name} - {operation.time} мин.',
                    size_hint_y=None,
                    height=25,
                )
            )

        card.add_widget(process_layout)
        self.content_layout.add_widget(card)

    def _add_zones_info_card(self):
        """Добавляет карточку с информацией о зонах цеха."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=300,
            padding=15,
            spacing=10,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Зоны цеха',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация о зонах
        zones_layout = BoxLayout(orientation='vertical', spacing=5)
        for zone_name, zone in self.workshop.zones.items():
            zones_layout.add_widget(
                MDLabel(
                    text=f'{zone_name}: {zone.area:.2f} м²',
                    size_hint_y=None,
                    height=25,
                )
            )

        card.add_widget(zones_layout)
        self.content_layout.add_widget(card)


class ResultWindow(Screen):
    """Окно ввода данных, обертка для TemplateInputWindow."""

    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result_window'
        # Создаем и добавляем TemplateInputWindow
        self.template_window = TemplateResultWindow(screen_manager=screen_manager)
        self.add_widget(self.template_window)

    @property
    def workshop(self):
        return self.template_window.workshop

    def set_workshop(self, workshop):
        """
        Устанавливает объект цеха и обновляет отображение.

        Args:
            workshop: Объект цеха с результатами расчета.
        """
        self.template_window.workshop = workshop


if __name__ == '__main__':

    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            initial_data_file = create_initial_data_file()
            reader = ExcelReader(initial_data_file)
            parameters_data = reader.read_parameters_data()
            process_data = reader.read_process_data()
            workshop = create_workshop_from_data(parameters_data, process_data)

            Window.minimum_width = 910
            Window.minimum_height = 500
            window = ResultWindow(debug_mode=True)
            window.workshop = workshop
            return window

    TestApp().run()
