#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from typing import Protocol

from design_of_mechanical_production.core.interfaces import IEquipment


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
