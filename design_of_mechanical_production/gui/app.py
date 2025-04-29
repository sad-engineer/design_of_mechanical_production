#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from design_of_mechanical_production.gui.settings_window import SettingsWindow
from design_of_mechanical_production.gui.input_window import InputWindow


class MainScreen(Screen):
    """Главный экран приложения."""
    pass


class MechanicalProductionApp(MDApp):
    """Главное приложение."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Устанавливаем цветовую схему по умолчанию
        self.theme_cls.primary_palette = "Blue"  # Основной цвет
        self.theme_cls.accent_palette = "Amber"  # Акцентный цвет
        self.theme_cls.theme_style = "Light"     # Светлая тема по умолчанию
        
        # Настраиваем цвета для светлой и темной темы
        self.theme_cls.material_style = "M3"     # Использовать Material Design 3
    
    def build(self):
        """Создает интерфейс приложения."""
        # Создаем менеджер экранов
        self.screen_manager = ScreenManager()
        
        # Создаем главный экран
        main_screen = MainScreen(name='main')
        
        # Создаем контейнер для основного контента
        main_layout = FloatLayout()
        
        # Создаем и добавляем окно ввода
        input_window = InputWindow()
        input_window.size_hint = (0.8, 0.8)
        input_window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        main_layout.add_widget(input_window)
        
        # Добавляем контейнер на главный экран
        main_screen.add_widget(main_layout)
        
        # Добавляем окно настроек
        settings_window = SettingsWindow(name='settings')
        self.screen_manager.add_widget(main_screen)
        self.screen_manager.add_widget(settings_window)
        
        # Устанавливаем размер окна
        Window.size = (800, 600)
        
        return self.screen_manager
    
    def toggle_theme(self, instance):
        """Переключает между светлой и темной темой."""
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
        
    def show_settings(self, instance):
        """Показывает окно настроек."""
        self.screen_manager.current = 'settings'


if __name__ == "__main__":
    MechanicalProductionApp().run() 
