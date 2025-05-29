#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button


class NotificationWindow:
    """
    Окно уведомлений с настраиваемыми кнопками и текстом.
    """

    def __init__(self, title: str, text: str, 
                 button1_text: str = "OK", button1_callback=None,
                 button2_text: str = "Отмена", button2_callback=None,
                 **kwargs):
        # Создаем основной контейнер
        content = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=5
        )

        # Добавляем текст
        label = MDLabel(
            text=text,
            size_hint_y=0.7,
            halign='center',
            valign='middle'
        )
        content.add_widget(label)

        # Создаем контейнер для кнопок
        button_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.3,
            spacing=20,
            padding=[0, 10, 0, 0],
            pos_hint={'center_x': 0.5}
        )

        # Создаем кнопки
        self.button1 = Button(
            text=button1_text,
            size_hint=(1, None),
            size=(120, 40)
        )
        if button1_callback:
            self.button1.bind(on_press=lambda x: self._handle_button(button1_callback))

        self.button2 = Button(
            text=button2_text,
            size_hint=(1, None),
            size=(120, 40)
        )
        if button2_callback:
            self.button2.bind(on_press=lambda x: self._handle_button(button2_callback))

        # Добавляем кнопки в контейнер
        button_box.add_widget(self.button1)
        button_box.add_widget(self.button2)
        content.add_widget(button_box)

        # Создаем всплывающее окно
        self.popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(400, 300),
            auto_dismiss=False,
        )

        # Устанавливаем начальный цвет фона
        self.popup.background_normal = ""
        app = MDApp.get_running_app()
        self.popup.background_color = app.theme_cls.bg_normal
        self.popup.title_color = app.theme_cls.bg_normal


    def _handle_button(self, callback):
        """Обрабатывает нажатие кнопки."""
        self.popup.dismiss()
        if callback:
            callback(None)

    def show(self):
        """Показывает окно уведомлений."""
        self.popup.open()

    @property
    def text(self):
        return self.popup.content.children[1].text

    @text.setter
    def text(self, value):
        self.popup.content.children[1].text = value


if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.core.window import Window

    class TestApp(MDApp):
        def build(self):
            self.theme_style = "Light"

            # Устанавливаем тему
            self.theme_cls.theme_style = self.theme_style
            Window.clearcolor = self.theme_cls.bg_normal

            # Создаем корневой виджет
            root = BoxLayout()

            # Создаем кнопку для демонстрации
            button = Button(
                text="Показать уведомление",
                size_hint=(0.5, 0.5),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            button.bind(on_press=self.show_notification)
            root.add_widget(button)

            # Создаем кнопку для смены темы
            theme_button = Button(
                text="Сменить тему",
                size_hint=(0.5, 0.5),
                pos_hint={'center_x': 0.5, 'center_y': 0.3}
            )
            theme_button.bind(on_press=self.toggle_theme)
            root.add_widget(theme_button)

            return root

        def toggle_theme(self, *args):
            """Переключает тему между светлой и темной."""
            self.theme_style = "Dark" if self.theme_style == "Light" else "Light"
            self.theme_cls.theme_style = self.theme_style
            Window.clearcolor = self.theme_cls.bg_normal

            # Обновляем цвет фона для всех открытых окон уведомлений
            for child in self.root.children:
                if isinstance(child, NotificationWindow):
                    child.popup.background = self.theme_cls.bg_normal

        def show_notification(self, instance):
            # Создаем окно уведомлений
            notification = NotificationWindow(
                title="Тестовое уведомление",
                text="Это пример использования окна уведомлений.\nМожно использовать многострочный текст.",
                button1_text="Сохранить",
                button1_callback=self.on_save,
                button2_text="Отмена",
                button2_callback=self.on_cancel
            )
            notification.show()

        def on_save(self, instance):
            print("Нажата кнопка 'Сохранить'")

        def on_cancel(self, instance):
            print("Нажата кнопка 'Отмена'")

    TestApp().run() 