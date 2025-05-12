#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Protocol

from design_of_mechanical_production.core.interfaces import IMachineInfo, IOperation


class IProcess(Protocol):
    """
    Интерфейс для технологического процесса.
    """

    operations: List['IOperation']

    def calculate_required_machines(self) -> None:
        """
        Рассчитывает необходимое количество станков.

        Args:
            production_volume: Объем производства

        Returns:
            Dict[str, IMachineInfo]: Словарь с информацией о станках
        """
        ...

    @property
    def machines(self) -> Dict[str, 'IMachineInfo']:
        """
        Количество станков по типам.
        """
        return ...

    @property
    def accepted_machines_count(self) -> int:
        """
        Общее количество станков.
        """
        return ...

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков.
        """
        return ...

    @property
    def total_time(self) -> Decimal:
        """
        Общее время на выполнение всех операций.
        """
        return ...

    @property
    def average_load_factor(self) -> Decimal:
        """
        Средний коэффициент загрузки станков.
        """
        return ...

    def calculate_percentage(self) -> None:
        """
        Рассчитывает долю от общей трудоемкости для каждой операции.
        """
        ...

    def add_operation(self, operation: 'IOperation') -> None:
        """
        Добавляет операцию в процесс.

        Args:
            operation: Операция для добавления
        """
        ...
