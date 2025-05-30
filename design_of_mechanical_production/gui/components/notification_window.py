#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class NotificationWindow:
    """
    Окно уведомлений с настраиваемыми кнопками и текстом.
    """

    def __init__(
        self,
        title: str,
        text: str,
        button1_text: str = "OK",
        button1_callback=None,
        button2_text: str = "Отмена",
        button2_callback=None,
        **kwargs,
    ):
        buttons = []
        app = MDApp.get_running_app()

        if button1_callback:
            buttons.append(
                MDFlatButton(
                    text=button1_text,
                    on_release=lambda x: self._handle_button(button1_callback),
                    md_bg_color=app.theme_cls.disabled_primary_color,
                )
            )

        if button2_callback:
            buttons.append(
                MDFlatButton(
                    text=button2_text,
                    on_release=lambda x: self._handle_button(button2_callback),
                    md_bg_color=app.theme_cls.disabled_primary_color,
                )
            )

        # Создаем диалоговое окно
        self.dialog = MDDialog(title=title, text=text, buttons=buttons)

    def _handle_button(self, callback):
        """Обрабатывает нажатие кнопки."""
        self.dialog.dismiss()
        if callback:
            callback(None)

    def show(self):
        """Показывает окно уведомлений."""
        self.dialog.open()

    @property
    def text(self):
        return self.dialog.text

    @text.setter
    def text(self, value):
        self.dialog.text = value


if __name__ == "__main__":
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    from kivymd.app import MDApp
    from kivymd.uix.button import MDRaisedButton

    class TestApp(MDApp):
        def build(self):
            self.theme_style = "Light"

            # Устанавливаем тему
            self.theme_cls.theme_style = self.theme_style
            Window.clearcolor = self.theme_cls.bg_normal

            # Создаем корневой виджет
            root = BoxLayout()

            # Создаем кнопку для демонстрации
            button = MDRaisedButton(
                text="Показать уведомление", size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            button.bind(on_press=self.show_notification)
            root.add_widget(button)

            # Создаем кнопку для смены темы
            theme_button = MDRaisedButton(
                text="Сменить тему", size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.3}
            )
            theme_button.bind(on_press=self.toggle_theme)
            root.add_widget(theme_button)

            return root

        def toggle_theme(self, *args):
            """Переключает тему между светлой и темной."""
            self.theme_style = "Dark" if self.theme_style == "Light" else "Light"
            self.theme_cls.theme_style = self.theme_style
            Window.clearcolor = self.theme_cls.bg_normal

        def show_notification(self, instance):
            # Создаем окно уведомлений
            notification = NotificationWindow(
                title="Тестовое уведомление",
                text="Это пример использования окна уведомлений.\nМожно использовать многострочный текст.",
                button1_text="Сохранить",
                button1_callback=self.on_save,
                button2_text="Отмена",
                button2_callback=self.on_cancel,
            )
            notification.show()

        def on_save(self, instance):
            print("Нажата кнопка 'Сохранить'")

        def on_cancel(self, instance):
            print("Нажата кнопка 'Отмена'")

    TestApp().run()
