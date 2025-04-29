#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton


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


class InputApp(App):
    def build(self):
        Window.size = (400, 300)
        return InputWindow()


if __name__ == '__main__':
    InputApp().run()
