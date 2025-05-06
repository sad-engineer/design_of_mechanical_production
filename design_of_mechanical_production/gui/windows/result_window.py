#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна отображения результатов расчета.
"""
from pathlib import Path

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from design_of_mechanical_production.data.output import TextReportGenerator
from design_of_mechanical_production.gui.windows.base_window import BaseWindow
from design_of_mechanical_production.settings import get_setting


class ResultWindow(BaseWindow):
    """
    Окно отображения результатов расчета.

    Attributes:
        screen_manager: Менеджер экранов приложения
        workshop: Объект цеха с результатами расчета
    """

    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.workshop = None
        self._init_ui()

    def _init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        self._create_header()
        self._create_content()
        self._create_buttons()

    def _create_header(self):
        """Создает заголовок окна."""
        # Создаем однострочный контейнер для иконок
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            width=40,
            height=40,
            padding=0,
            spacing=5,
            pos=(Window.width - 100, Window.height - 50),
        )

        # Добавляем иконки
        self.theme_btn = MDIconButton(
            icon="theme-light-dark", size_hint=(None, None), size=(40, 40), padding=0, on_release=self.toggle_theme
        )
        self.header.add_widget(self.theme_btn)

        self.settings_btn = MDIconButton(
            icon="cog", size_hint=(None, None), size=(40, 40), padding=0, on_release=self.open_settings
        )
        self.header.add_widget(self.settings_btn)

        self.add_widget(self.header)

        # Добавляем заголовок
        self.label = MDLabel(
            text='Результаты расчета',
            size_hint=(1.25, None),
            height=50,
            pos=(0, Window.height - 50),
            halign='center',
            font_style='H5',
        )
        self.add_widget(self.label)

        # Привязываем обновление позиции к изменению размера окна
        Window.bind(size=self._update_header_position)

    def _update_header_position(self, instance, size):
        """Обновляет позицию header при изменении размера окна."""
        width, height = size
        self.header.pos = (width - 100, height - 50)
        self.label.pos = (0, height - 50)

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

        scroll_view.add_widget(self.content_layout)
        self.add_widget(scroll_view)

    def _create_buttons(self):
        """Создает кнопки управления."""
        # Контейнер для кнопок
        buttons_box = BoxLayout(
            orientation='horizontal',
            size_hint=(0.5, None),
            height=50,
            spacing=5,
            padding=[0, 0, 0, 5],
            pos_hint={'center_x': 0.5, 'bottom': 0},
        )

        # Кнопки
        back_btn = Button(text='Назад', size_hint_x=0.5, height=40, on_release=self.back_to_input)
        export_btn = Button(text='Экспорт', size_hint_x=0.5, height=40, on_release=self.export_results)
        buttons_box.add_widget(back_btn)
        buttons_box.add_widget(export_btn)
        self.add_widget(buttons_box)

    def set_workshop(self, workshop):
        """
        Устанавливает объект цеха и обновляет отображение.

        Args:
            workshop: Объект цеха с результатами расчета.
        """
        self.workshop = workshop
        self._update_content()

    def _update_content(self):
        """Обновляет отображение результатов расчета."""
        if not self.workshop:
            return

        # Очищаем предыдущий контент
        self.content_layout.clear_widgets()

        # Создаем карточки с результатами
        self._add_general_info_card()
        self._add_zones_info_card()
        self._add_process_info_card()

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
                text='Общая информация',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация
        info_layout = BoxLayout(orientation='vertical', spacing=5)
        info_layout.add_widget(MDLabel(text=f'Название цеха: {self.workshop.name}'))
        info_layout.add_widget(MDLabel(text=f'Годовой объем производства: {self.workshop.production_volume} шт.'))
        info_layout.add_widget(MDLabel(text=f'Масса детали: {self.workshop.mass_detail} кг'))
        info_layout.add_widget(MDLabel(text=f'Общая площадь цеха: {self.workshop.total_area:.2f} м²'))

        card.add_widget(info_layout)
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

    def back_to_input(self, instance):
        """
        Возвращает к окну ввода данных.

        Args:
            instance: Экземпляр кнопки
        """
        if self.screen_manager:
            # Очищаем данные цеха перед возвратом
            self.workshop = None
            self.content_layout.clear_widgets()
            # Переключаемся на экран ввода
            self.screen_manager.current = 'main'

    def export_results(self, instance):
        """
        Экспортирует результаты расчета в текстовый отчет.

        Args:
            instance: Экземпляр кнопки
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
