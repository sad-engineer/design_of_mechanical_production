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
    def add_row(self, row_widgets: List[Any]):
        """Добавляет строку в таблицу."""
        pass

    @abstractmethod
    def add_empty_row(self):
        """Добавляет пустую строку в таблицу."""
        pass

    @abstractmethod
    def bind_row_events(self, row_widgets: List[Any]):
        """
        Связывает события с строками.

        Args:
            row_widgets: Список виджетов строки.
        """
        pass

    @abstractmethod
    def on_row_text_changed(self, row: List[Any], value: str):
        """
        Обрабатывает изменения в строке.

        Args:
            row: Список виджетов измененной строки.
            value: Новое значение.
        """
        pass

    @abstractmethod
    def on_row_changed(self, row_index: int, data: List[str]):
        """
        Обрабатывает изменение строки.

        Args:
            row_index: Индекс измененной строки.
            data: Новые данные строки.
        """
        pass
