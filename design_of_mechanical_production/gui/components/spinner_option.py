#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс опции для выпадающего списка.
"""
from kivy.uix.spinner import SpinnerOption


class MySpinnerOption(SpinnerOption):
    """
    Опция для выпадающего списка с настраиваемой высотой.
    """

    def __init__(self, **kwargs):
        """
        Инициализирует опцию выпадающего списка.

        Args:
            **kwargs: Дополнительные аргументы для SpinnerOption.
        """
        super().__init__(**kwargs)
        self.height = 20
