#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class MachineToolSuggestField(BoxLayout):
    """
    Поле с автодополнением для выбора станка.

    Attributes:
        machine_tools_names: Список доступных станков.
        text_input: Текстовое поле для ввода.
        suggestions_layout: Layout для отображения подсказок.
    """

    def __init__(self, text: str, **kwargs):
        """
        Инициализирует поле с автодополнением.

        Args:
            machine_tools_names: Список доступных станков.
            **kwargs: Дополнительные аргументы для BoxLayout.
        """
        super().__init__(orientation='vertical', size_hint_y=None, height=30, **kwargs)
        self.machine_tools_names = ["16К20", "16К20Ф3", "16К20Ф3С32", "16К20Ф3С5", "16К20Ф3С32", "16К20Ф3С5"]
        self.text_input = TextInput(text=text, size_hint_y=None, height=30, multiline=False)
        self.text_input.bind(text=self.on_text)
        self.add_widget(self.text_input)
        self.suggestions_layout = None

    def on_text(self, instance: TextInput, value: str):
        """
        Обрабатывает изменение текста в поле ввода.

        Args:
            instance: Экземпляр TextInput
            value: Новое значение текста
        """
        self.remove_suggestions()

        filtered = self.machine_tools_names
        if len(value) >= 1:
            filtered = [tool for tool in self.machine_tools_names if value.lower() in tool.lower()]

        if len(filtered) < 2:
            return

        if filtered:
            max_rows = 5
            row_height = 30
            max_height = max_rows * row_height
            content_height = row_height * len(filtered)
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=content_height)
            for tool in filtered:
                btn = Button(text=tool, size_hint_y=None, height=row_height)
                btn.bind(on_release=lambda btn, name=tool: self.select_tool(name))
                box.add_widget(btn)
            scroll = ScrollView(
                size_hint=(None, None), size=(self.text_input.width, min(max_height, content_height)), bar_width=8
            )
            scroll.add_widget(box)
            self.suggestions_layout = scroll
            x_win, y_win = self.text_input.to_window(self.text_input.x, self.text_input.y)
            self.suggestions_layout.pos = (x_win, y_win - self.suggestions_layout.height)
            Window.add_widget(self.suggestions_layout)

    def remove_suggestions(self):
        """Удаляет отображение подсказок."""
        if self.suggestions_layout and self.suggestions_layout.parent:
            Window.remove_widget(self.suggestions_layout)
        self.suggestions_layout = None

    def select_tool(self, tool: str):
        """
        Выбирает станок из подсказок.

        Args:
            tool: Название выбранного станка.
        """
        self.text_input.text = tool
        self.remove_suggestions()

    @property
    def text(self) -> str:
        """
        Возвращает текст из поля ввода.

        Returns:
            str: Текст из поля ввода.
        """
        return self.text_input.text

    @text.setter
    def text(self, value: str):
        """
        Устанавливает текст в поле ввода.

        Args:
            value: Новое значение текста.
        """
        self.text_input.text = value
