#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TableConfig:
    """
    Конфигурация таблицы.

    Attributes:
    headers: Список заголовков столбцов.
    column_widths: Список ширин столбцов.
    initial_data: Начальные данные таблицы.
    operations: Список доступных операций.
    """

    headers: List[str]
    column_widths: List[Optional[int]]
    initial_data: List[List[str]]
