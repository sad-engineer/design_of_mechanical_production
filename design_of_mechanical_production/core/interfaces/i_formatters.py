#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import List, Protocol


class INumberFormatter(Protocol):
    """
    Интерфейс для форматирования чисел.
    """

    def format(self, number: Decimal, precision: int = 3) -> str:
        """
        Форматирует число.

        Args:
            number: Число для форматирования
            precision: Точность

        Returns:
            str: Отформатированное число
        """
        ...


class ITableFormatter(Protocol):
    """
    Интерфейс для форматирования таблиц.
    """

    def format(self, headers: List[str], data: List[tuple], total_row: tuple) -> List[str]:
        """
        Форматирует таблицу.

        Args:
            headers: Заголовки колонок
            data: Данные для строк
            total_row: Данные для строки итога

        Returns:
            List[str]: Отформатированная таблица
        """
        ...
