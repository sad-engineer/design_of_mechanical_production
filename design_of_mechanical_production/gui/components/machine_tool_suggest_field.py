#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class Tooltip(BoxLayout):
    """Всплывающая подсказка."""

    def __init__(self, text: str, **kwargs):
        super().__init__(orientation='vertical', size_hint=(None, None), **kwargs)
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 0.9)  # Темно-серый цвет с прозрачностью
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

        self.label = Label(
            text=text,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 35),
            text_size=(200, 30),
            halign='left',
            valign='middle',
            padding=(5, 0),
        )
        self.add_widget(self.label)
        self.size = self.label.size

    def _update_rect(self, instance, value):
        """Обновляет размер и позицию фона при изменении размера или позиции виджета."""
        self.rect.pos = instance.pos
        self.rect.size = instance.size


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
        self.text_input.bind(on_touch_down=self._on_touch_down)
        self.add_widget(self.text_input)
        self.suggestions_layout = None
        self.tooltip = None

    def _on_touch_down(self, instance, touch):
        """
        Обрабатывает нажатие мыши на поле ввода.

        Args:
            instance: Экземпляр TextInput
            touch: Объект касания
        """
        if instance.collide_point(*touch.pos) and touch.button == 'right':
            self.clear_value()
            return True
        return False

    def clear_value(self):
        """Очищает поле ввода."""
        self.text_input.text = ""
        self.remove_suggestions()
        self.remove_tooltip()

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

    def show_tooltip(self, text: str):
        """
        Показывает всплывающую подсказку.

        Args:
            text: Текст подсказки
        """
        self.remove_tooltip()
        self.tooltip = Tooltip(text)
        x_win, y_win = self.text_input.to_window(self.text_input.x, self.text_input.y)
        self.tooltip.pos = (x_win, y_win + self.text_input.height)
        Window.add_widget(self.tooltip)

    def remove_tooltip(self):
        """Удаляет всплывающую подсказку."""
        if self.tooltip and self.tooltip.parent:
            Window.remove_widget(self.tooltip)
        self.tooltip = None

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
        self.remove_tooltip()

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

    def set_style(self, style: str):
        """
        Устанавливает стиль текстового поля.

        Args:
            style: Стиль поля ('normal' или 'error')
        """
        if style == "error":
            self.text_input.background_color = (1, 0.8, 0.8, 1)
        else:
            self.text_input.background_color = (1, 1, 1, 1)
