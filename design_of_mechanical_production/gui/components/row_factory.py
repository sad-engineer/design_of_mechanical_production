#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List

from design_of_mechanical_production.gui.components.interfaces import TableRowFactory
from design_of_mechanical_production.gui.components.table_row import TableRow


class BaseTableRowFactory(TableRowFactory):
    """
    Базовая реализация фабрики строк таблицы.
    """

    def create_row(self, row_data: List[str] = None, machine_name_replace: bool = True) -> List[Any]:
        """
        Создает новую строку таблицы.

        Args:
            row_data: Данные для инициализации строки. Если None, создается пустая строка.
            machine_name_replace: Флаг для замены названия станка.
                Если True, проверяет имя станка из row_data на соответствие перечню разрешенных станков для операции.
                При не соответствии, возьмет первый станок из разрешенного списка

        Returns:
            List[Any]: Список виджетов строки.
        """
        row = TableRow(row_data, machine_name_replace)
        return row.get_widgets()
