#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from typing import Protocol


class IEquipmentFactory(Protocol):
    """
    Интерфейс для фабрики оборудования.
    """

    def create_equipment(self, model: str) -> 'IEquipment':
        """
        Создает объект оборудования.

        Args:
            model: Модель оборудования

        Returns:
            IEquipment: Объект оборудования
        """
        ...
