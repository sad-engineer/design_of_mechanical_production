#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.uix.textinput import TextInput


class CustomizedTextInput(TextInput):
    """
    Поле ввода номера операции.
    """

    def __init__(self, text: str, **kwargs):
        super().__init__(text=text)
        self.multiline = False
        self.size_hint_y = None
        self.height = 30
        self.halign = 'center'
        self.bind(text=self._on_text_changed)

    def _on_text_changed(self, instance, value):
        self.set_value(value)

    def set_value(self, string):
        """Устанавливает значение поля ввода."""
        self.text = string.replace(' ', '')

    def get_value(self):
        """Возвращает значение поля ввода."""
        return self.text

    def clear_value(self):
        """Очищает значение поля ввода."""
        self.text = ""


class TimeTextInput(CustomizedTextInput):
    """
    Текстовое поле для ввода времени.
    Разрешает ввод только цифр, запятой и точки.
    """

    def insert_text(self, substring: str, from_undo: bool = False) -> str:
        """
        Обрабатывает вставку текста в поле.

        Args:
            substring: Вставляемый текст.
            from_undo: Флаг, указывающий, что вставка происходит при отмене действия.

        Returns:
            str: Обработанный текст для вставки.
        """
        # Разрешаем ввод только цифр, запятой и точки (которая будет заменена на запятую)
        s = ''.join([c for c in substring if c.isdigit() or c in '.,'])
        # Заменяем точку на запятую
        s = s.replace('.', ',')

        # Проверяем, будет ли текст валидным после вставки
        new_text = self.text + s
        if not self.filter_text(new_text):
            return ''  # Если текст невалидный, отменяем вставку

        return super().insert_text(s, from_undo=from_undo)

    @staticmethod
    def filter_text(text: str) -> bool:
        """
        Фильтрует вводимый текст.

        Args:
            text: Текст для проверки.

        Returns:
            bool: True, если текст допустим, иначе False.
        """
        # Разрешаем только одну запятую
        if text.count(',') > 1:
            return False
        return True
