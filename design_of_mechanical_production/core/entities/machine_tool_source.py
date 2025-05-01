#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from machine_tools import MachineTool
from machine_tools import MachineToolsContainer as Container


@dataclass
class MachineTool:
    """
    Класс, представляющий станок.
    """

    model: str
    length: float
    width: float
    height: float
    automation: str
    weight: float
    power_lathe_passport_kvt: float


class MachineToolSource:
    """
    Базовый класс для источников данных о станках.
    """

    @staticmethod
    def get_machine_tool(model_name: str) -> Optional[MachineTool]:
        """
        Получает информацию о станке по модели.

        Args:
            model_name: Модель станка

        Returns:
            Optional[MachineTool]: Информация о станке или None
        """
        raise NotImplementedError


class DatabaseMachineToolSource(MachineToolSource):
    """
    Источник данных о станках из базы данных.
    """

    @staticmethod
    def get_machine_tool(model_name: str) -> MachineTool:
        """
        Получает данные об оборудовании из базы данных.

        Args:
            model_name: Имя модели оборудования

        Returns:
            Объект с данными об оборудовании

        Raises:
            TypeError: Если оборудование не найдено в базе данных
        """
        creator = Container().creator()
        return creator.by_name(model_name)


class DefaultMachineToolSource(MachineToolSource):
    """
    Источник данных о станках по умолчанию.
    """

    @staticmethod
    def get_machine_tool(model_name: str) -> MachineTool:
        """
        Возвращает данные об оборудовании по умолчанию.

        Args:
            model_name: Имя модели оборудования

        Returns:
            Объект с данными об оборудовании

        Raises:
            ValueError: Если модель не поддерживается
        """
        if model_name == "DMG CTX beta 2000":
            return MachineTool(
                model="DMG CTX beta 2000",
                length=Decimal("6234"),
                width=Decimal("3210"),
                height=Decimal("2052"),
                automation="Автоматическая",
                weight=Decimal(10000.0),
                power_lathe_passport_kvt=Decimal(35.0),
            )
        raise ValueError(f"Модель {model_name} не поддерживается")
