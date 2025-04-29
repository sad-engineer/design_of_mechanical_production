#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.icon_definitions import md_icons


class InputWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 0
        self.padding = 0
        
        # Создаем контейнер для заголовка
        anchor_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='top',
            size_hint_y=None,
            height=30
        )
        
        # Горизонтальный контейнер для заголовка и иконок
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=30,
            spacing=10,
            padding=[10, 0, 10, 0]
        )
        
        # Заголовок
        header_layout.add_widget(MDLabel(
            text='Ввод начальных условий',
            size_hint_x=None,
            width=250,
            halign='center',
            valign='middle'
        ))
        
        # Добавляем растягивающийся виджет для заполнения пространства
        header_layout.add_widget(BoxLayout())
        
        # Иконки
        self.theme_button = MDIconButton(
            icon="theme-light-dark",
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={'center_y': 0.5}
        )
        header_layout.add_widget(self.theme_button)
        
        self.settings_button = MDIconButton(
            icon="cog",
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={'center_y': 0.5}
        )
        header_layout.add_widget(self.settings_button)
        
        # Добавляем header_layout в anchor_layout
        anchor_layout.add_widget(header_layout)
        
        # Добавляем anchor_layout в основной контейнер
        self.add_widget(anchor_layout)
        
        # Основной контейнер для содержимого
        content_layout = BoxLayout(
            orientation='vertical',
            padding=[20, 20, 20, 20],
            spacing=10
        )
        
        # Название цеха
        content_layout.add_widget(MDLabel(
            text='Название цеха:',
            size_hint_y=None,
            height=30
        ))
        self.name_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_color=(1, 1, 1, 1) if MDApp.get_running_app().theme_cls.theme_style == "Light" else (0.2, 0.2, 0.2, 1)
        )
        content_layout.add_widget(self.name_input)
        
        # Годовой объем производства
        content_layout.add_widget(MDLabel(
            text='Годовой объем производства (шт.):',
            size_hint_y=None,
            height=30
        ))
        self.volume_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_color=(1, 1, 1, 1) if MDApp.get_running_app().theme_cls.theme_style == "Light" else (0.2, 0.2, 0.2, 1)
        )
        content_layout.add_widget(self.volume_input)
        
        # Масса детали
        content_layout.add_widget(MDLabel(
            text='Масса детали (кг):',
            size_hint_y=None,
            height=30
        ))
        self.mass_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=30,
            background_color=(1, 1, 1, 1) if MDApp.get_running_app().theme_cls.theme_style == "Light" else (0.2, 0.2, 0.2, 1)
        )
        content_layout.add_widget(self.mass_input)
        
        # Кнопки управления
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.save_button = Button(
            text='Сохранить',
        )
        self.save_button.bind(on_press=self.save_data)
        button_layout.add_widget(self.save_button)
        
        self.cancel_button = Button(
            text='Отмена',
        )
        self.cancel_button.bind(on_press=self.cancel)
        button_layout.add_widget(self.cancel_button)
        
        content_layout.add_widget(button_layout)
        self.add_widget(content_layout)
        
        # Установка начальных значений
        self.name_input.text = 'Механический цех №1'
        self.volume_input.text = '10000'
        self.mass_input.text = '112.8'
    
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


class InputApp(App):
    def build(self):
        Window.size = (400, 300)
        return InputWindow()


if __name__ == '__main__':
    InputApp().run()
