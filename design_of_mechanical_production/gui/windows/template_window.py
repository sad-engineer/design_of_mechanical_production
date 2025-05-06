#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит шаблонный класс окна с базовой структурой.
"""
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel


class TemplateWindow(FloatLayout):
    """
    Шаблонное окно с базовой структурой.

    Attributes:
        screen_manager: Менеджер экранов приложения.
        debug_mode: Режим отладки.
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self.debug_mode = debug_mode
        self._init_ui()

    def _init_ui(self):
        """Инициализирует пользовательский интерфейс."""
        if self.debug_mode:
            with self.canvas.before:
                Color(1, 0, 0, 0.3)  # Красный с прозрачностью
                self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_rect, size=self._update_rect)

        self._create_header()
        self._create_content()
        self._create_buttons()

    def _update_rect(self, instance, value):
        """Обновляет размер и позицию отладочного прямоугольника."""
        if self.debug_mode:
            self.rect.pos = instance.pos
            self.rect.size = instance.size

    def _create_header(self):
        """Создает заголовок окна."""
        # Создаем контейнер для иконок и заголовка
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=50,
            padding=[10, 5, 10, 5],
            spacing=5,
            pos_hint={'top': 1},
        )
        if self.debug_mode:
            with self.header.canvas.before:
                self._header_color = Color(0, 1, 0, 0.3)  # Зеленый с прозрачностью
                self._header_rect = Rectangle(pos=self.header.pos, size=self.header.size)
            self.header.bind(pos=self._update_header_debug, size=self._update_header_debug)

        # Добавляем иконки
        self.theme_btn = MDIconButton(
            icon="theme-light-dark", size_hint=(None, None), size=(40, 40), padding=0, on_release=self.toggle_theme
        )
        self.settings_btn = MDIconButton(
            icon="cog", size_hint=(None, None), size=(40, 40), padding=0, on_release=self.open_settings
        )

        # Добавляем заголовок
        self.label = MDLabel(
            text='Заголовок окна',
            size_hint=(1, 1),
            halign='center',
            font_style='H5',
            valign='middle',
        )

        self.header.add_widget(self.label)
        self.header.add_widget(self.settings_btn)
        self.header.add_widget(self.theme_btn)

        self.add_widget(self.header)

    def _update_header_debug(self, instance, value):
        """Обновляет размер и позицию отладочного прямоугольника заголовка."""
        if self.debug_mode:
            self._header_rect.pos = instance.pos
            self._header_rect.size = instance.size

    def _update_header_position(self, instance, size):
        """Обновляет позицию header при изменении размера окна."""
        # header теперь с size_hint, позиция обновляется автоматически
        self.label.pos = (0, size[1] - 50)

    def _create_content(self):
        """Создает основной контент окна."""
        # Создаем контейнер для содержимого
        self.content = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=10,
            spacing=10,
        )

        if self.debug_mode:
            with self.content.canvas.before:
                Color(0, 0, 1, 0.3)  # Синий с прозрачностью
                Rectangle(pos=self.content.pos, size=self.content.size)
            self.content.bind(pos=self._update_content_debug, size=self._update_content_debug)

        self.add_widget(self.content)

    def _update_content_debug(self, instance, value):
        """Обновляет размер и позицию отладочного прямоугольника контента."""
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 1, 0.3)
                Rectangle(pos=instance.pos, size=instance.size)

    def _create_buttons(self):
        """Создает кнопки управления."""
        # Контейнер для кнопок
        self.buttons_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, None),
            height=50,
            spacing=5,
            padding=[0, 0, 0, 5],
            pos_hint={'x': 0, 'y': 0},
        )

        if self.debug_mode:
            with self.buttons_box.canvas.before:
                Color(1, 1, 0, 0.3)  # Желтый с прозрачностью
                Rectangle(pos=self.buttons_box.pos, size=self.buttons_box.size)
            self.buttons_box.bind(pos=self._update_buttons_debug, size=self._update_buttons_debug)

        # Кнопки с ограничением максимальной ширины
        self.max_button_width = 200
        self.button1 = Button(text='Кнопка 1', size_hint=(None, 1), width=self.max_button_width)
        self.button2 = Button(text='Кнопка 2', size_hint=(None, 1), width=self.max_button_width)
        self.buttons_box.add_widget(self.button1)
        self.buttons_box.add_widget(self.button2)
        self.add_widget(self.buttons_box)

        # Центрирование кнопок и ограничение ширины при изменении размера контейнера
        self.buttons_box.bind(size=self._update_buttons_width)

    def _update_buttons_debug(self, instance, value):
        """Обновляет размер и позицию отладочного прямоугольника кнопок."""
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 0, 0.3)
                Rectangle(pos=instance.pos, size=instance.size)

    def _update_buttons_width(self, instance, value):
        """Ограничивает максимальную ширину кнопок и центрирует их в контейнере для любого количества кнопок."""
        buttons = [w for w in self.buttons_box.children if isinstance(w, Button)]
        num_buttons = len(buttons)
        if num_buttons == 0:
            return
        total_spacing = self.buttons_box.spacing * (num_buttons - 1)
        total_max_width = num_buttons * self.max_button_width + total_spacing
        if instance.width >= total_max_width:
            # Все кнопки максимальной ширины, центрируем
            for btn in buttons:
                btn.width = self.max_button_width
            left_padding = (instance.width - total_max_width) / 2
            self.buttons_box.padding = [left_padding, 5, left_padding, 5]
        else:
            # Кнопки делят доступное пространство поровну
            btn_width = (instance.width - total_spacing) / num_buttons
            for btn in buttons:
                btn.width = btn_width
            self.buttons_box.padding = [0, 5, 0, 5]

    @staticmethod
    def cancel(instance):
        """
        Отменяет ввод данных и завершает работу приложения.

        Args:
            instance: Экземпляр кнопки
        """
        # Завершаем работу приложения
        MDApp.get_running_app().stop()

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
            Window.size = (800, 600)
            window = TemplateWindow(debug_mode=True)

            # Переопределяем имя и функцию button1
            window.button1.text = "ОК"
            window.button1.bind(on_release=lambda instance: print("Нажата кнопка 'OK'"))

            window.button2.text = "Cancel"
            window.button2.bind(on_release=lambda instance: print("Нажата кнопка 'Cancel'"))

            # Пример добавления дополнительной кнопки
            extra_button = Button(
                text='Доп. кнопка',
                size_hint=(None, 1),
                width=window.max_button_width,
                on_release=lambda instance: print('Нажата доп. кнопка'),
            )
            window.buttons_box.add_widget(extra_button)

            return window

    TestApp().run()
