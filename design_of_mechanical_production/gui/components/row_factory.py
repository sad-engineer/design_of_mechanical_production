#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List

from design_of_mechanical_production.gui.components.interfaces import TableRowFactory
from design_of_mechanical_production.gui.components.table_row import TableRow


class BaseTableRowFactory(TableRowFactory):
    """
    Базовая реализация фабрики строк таблицы.

    Attributes:
        operations: Список доступных операций.
    """

    def __init__(self, operations: List[str]):
        """
        Инициализирует фабрику строк.

        Args:
            operations: Список доступных операций.
        """
        self.operations = operations

    def create_row(self, row_data: List[str] = None) -> List[Any]:
        """
        Создает новую строку таблицы.

        Args:
            row_data: Данные для инициализации строки. Если None, создается пустая строка.

        Returns:
            List[Any]: Список виджетов строки.
        """
        row = TableRow(row_data)
        return row.get_widgets()
