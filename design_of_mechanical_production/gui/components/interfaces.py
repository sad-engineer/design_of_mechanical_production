#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import Any, List, Optional


class TableDataProvider(ABC):
    """Интерфейс для поставщика данных таблицы."""

    @abstractmethod
    def get_headers(self) -> List[str]:
        """Возвращает список заголовков столбцов."""
        pass

    @abstractmethod
    def get_column_widths(self) -> List[Optional[int]]:
        """Возвращает список ширин столбцов."""
        pass

    @abstractmethod
    def get_initial_data(self) -> List[List[str]]:
        """Возвращает начальные данные таблицы."""
        pass


class TableOperationsProvider(ABC):
    """Интерфейс для поставщика доступных операций."""

    @abstractmethod
    def get_available_operations(self) -> List[str]:
        """Возвращает список доступных операций."""
        pass


class TableRowFactory(ABC):
    """Интерфейс для фабрики создания строк таблицы."""

    @abstractmethod
    def create_row(self, data: List[str] = None) -> List[Any]:
        """
        Создает новую строку таблицы.

        Args:
            data: Данные для инициализации строки. Если None, создается пустая строка.

        Returns:
            List[Any]: Список виджетов строки.
        """
        pass


class TableEventManager(ABC):
    """Интерфейс для менеджера событий таблицы."""

    @abstractmethod
    def on_row_changed(self, row_index: int, data: List[str]):
        """
        Обрабатывает изменение строки.

        Args:
            row_index: Индекс измененной строки.
            data: Новые данные строки.
        """
        pass
