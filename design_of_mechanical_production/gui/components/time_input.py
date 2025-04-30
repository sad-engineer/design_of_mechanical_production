#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс текстового поля для ввода времени.
"""
from kivy.uix.textinput import TextInput


class TimeTextInput(TextInput):
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
