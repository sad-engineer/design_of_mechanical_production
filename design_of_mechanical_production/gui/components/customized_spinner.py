#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Callable, List

from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

from design_of_mechanical_production.gui.components.customized_spinner_option import CustomizedSpinnerOption


class CustomizedSpinner(Spinner):
    """
    Спиннер для выбора операции.
    """

    def __init__(self, text: str, items: List[str], on_item_selected: Callable, **kwargs):
        super().__init__(text=text, **kwargs)
        self.values = items
        self.size_hint_y = None
        self.height = 30
        # self.background_normal = ''
        self.background_color = (0.6, 0.6, 0.6, 1)
        self.option_cls = CustomizedSpinnerOption

        # Добавляем настройку выпадающего списка
        self.dropdown_cls = DropDown
        self.dropdown_cls.max_height = 210  # Максимальная высота выпадающего списка

        # функция внешнего приложения, которая вызывается при выборе элемента списка
        self.on_item_selected = on_item_selected
        # при выборе операции, выполняется функция внешне
        self.bind(text=self._on_text_changed)

    def _on_text_changed(self, instance, value):
        self.on_item_selected(value)

    def set_value(self, string):
        """Устанавливает значение поля ввода."""
        self.text = string

    def get_value(self):
        """Возвращает значение поля ввода."""
        return self.text

    def clear_value(self):
        """Очищает значение поля ввода."""
        self.text = ""
