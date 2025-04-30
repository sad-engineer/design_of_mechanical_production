#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List
from design_of_mechanical_production.gui.components.interfaces import TableEventManager
from design_of_mechanical_production.gui.components.table import EditableTable


class TableEventManagerImpl(TableEventManager):
    """
    Реализация менеджера событий таблицы.
    
    Attributes:
        table: Экземпляр таблицы, для которой обрабатываются события.
    """
    
    def __init__(self, table: EditableTable):
        """
        Инициализирует менеджер событий.
        
        Args:
            table: Экземпляр таблицы, для которой обрабатываются события.
        """
        self.table = table

    def on_row_changed(self, row_index: int, data: List[str]):
        """
        Обрабатывает изменение строки.
        
        Args:
            row_index: Индекс измененной строки.
            data: Новые данные строки.
        """
        if row_index == len(self.table.table_rows) - 1 and any(data):
            self.table.add_empty_row()
