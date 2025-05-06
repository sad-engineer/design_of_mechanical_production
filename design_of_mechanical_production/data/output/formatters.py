#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import List

from design_of_mechanical_production.core.interfaces import INumberFormatter, ITableFormatter


class NumberFormatter(INumberFormatter):
    """
    Реализация форматирования чисел.

    """

    def format(self, number: Decimal, precision: int = 3) -> str:
        """
        Форматирует число с 3 знаками после запятой. Если после запятой нет значащих цифр, то не добавляет нули.
        """
        # Сначала округляем число до указанной точности
        rounded = round(number, precision)

        # Проверяем, является ли число целым
        if rounded == rounded.to_integral_value():
            return f"{int(rounded)}"

        # Преобразуем в строку с максимальной точностью
        str_num = f"{rounded:.{precision}f}"

        # Удаляем последовательность нулей в конце дробной части
        if '.' in str_num:
            str_num = str_num.rstrip('0').rstrip('.')

        # Заменяем точку на запятую
        return str_num.replace('.', ',')


class TableFormatter(ITableFormatter):
    """
    Реализация форматирования таблиц.
    """

    def format(self, headers: List[str], data: List[tuple], total_row: tuple) -> List[str]:
        """
        Форматирует таблицу с заголовками, данными и строкой итога.
        """
        table = list()
        # Добавляем разделительную линию
        table.append("+" + "+".join("-" * 20 for _ in headers) + "+")
        # Добавляем заголовки
        table.append("|" + "|".join(f"{header:^20}" for header in headers) + "|")
        # Добавляем разделительную линию
        table.append("+" + "+".join("-" * 20 for _ in headers) + "+")

        # Добавляем данные
        for row in data:
            table.append("|" + "|".join(f"{cell:^20}" for cell in row) + "|")

        # Добавляем разделительную линию
        table.append("+" + "+".join("-" * 20 for _ in headers) + "+")
        # Добавляем строку итога
        table.append("|" + "|".join(f"{cell:^20}" for cell in total_row) + "|")
        # Добавляем нижнюю границу таблицы
        table.append("+" + "+".join("-" * 20 for _ in headers) + "+")

        return table
