#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль с основным классом приложения.
"""

from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from design_of_mechanical_production.gui.windows import InputWindow, ResultWindow, SettingsWindow


class MainScreen(Screen):
    """Главный экран приложения."""

    pass


class WorkshopDesignApp(MDApp):
    """
    Основной класс приложения.

    Attributes:
        theme_cls: Класс для управления темой приложения
    """

    def __init__(self, theme: str = "Light", **kwargs):
        """
        Инициализирует приложение.

        Args:
            config: Конфигурация приложения
            **kwargs: Дополнительные аргументы
        """
        super().__init__(**kwargs)

        # Устанавливаем тему
        self.theme_cls.theme_style = theme

        # Устанавливаем размер окна
        Window.minimum_width = 910
        Window.minimum_height = 500

        # Устанавливаем цветовую схему по умолчанию
        self.theme_cls.primary_palette = "Blue"  # Основной цвет
        self.theme_cls.accent_palette = "Amber"  # Акцентный цвет
        self.theme_cls.material_style = "M3"  # Использовать Material Design 3

    def build(self) -> MDScreen:
        """
        Создает и возвращает корневой виджет приложения.

        Returns:
            MDScreen: Корневой виджет приложения
        """
        # Устанавливаем название приложения
        self.title = "Расчет площади цеха"

        # Создаем менеджер экранов
        self.screen_manager = ScreenManager()

        # Создаем главный экран
        main_screen = MainScreen(name='main')

        # Создаем контейнер для основного контента
        main_layout = FloatLayout()

        # Создаем и добавляем окно ввода
        input_window = InputWindow(screen_manager=self.screen_manager)
        input_window.size_hint = (0.8, 0.8)
        input_window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        main_layout.add_widget(input_window)

        # Добавляем контейнер на главный экран
        main_screen.add_widget(main_layout)

        # Добавляем окно настроек
        settings_window = SettingsWindow(name='settings')
        result_window = ResultWindow(name='result', screen_manager=self.screen_manager)
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(settings_window)
        self.screen_manager.add_widget(result_window)

        # Устанавливаем размер окна
        Window.size = (800, 600)

        return self.screen_manager

    def toggle_theme(self, instance):
        """Переключает между светлой и темной темой."""
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def show_settings(self, instance):
        """Показывает окно настроек."""
        self.screen_manager.current = 'settings'


if __name__ == "__main__":
    WorkshopDesignApp().run()
