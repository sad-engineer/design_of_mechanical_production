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
from design_of_mechanical_production.settings import get_setting
from design_of_mechanical_production.gui.windows.template_window import TemplateWindow


class ResultWindow1(TemplateWindow):
    """
    Окно отображения результатов расчета.

    Attributes:
        screen_manager: Менеджер экранов приложения
        workshop: Объект цеха с результатами расчета
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)
        self.screen_manager = screen_manager
        self.workshop = None
        # self._init_ui()

    def _init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        self._create_content()

    def _create_content(self):
        """Создает основной контент с результатами."""
        # Создаем ScrollView для прокрутки контента
        scroll_view = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            do_scroll_x=False,
        )
        self.add_widget(scroll_view)

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


if __name__ == '__main__':
    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            Window.minimum_width = 910
            Window.minimum_height = 500
            window = ResultWindow1(debug_mode=True)
            return window

    TestApp().run()
