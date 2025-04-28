#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Protocol
from decimal import Decimal
from machine_tools import MachineTool, MachineToolsContainer as Container


class MachineToolSource(Protocol):
    """
    Интерфейс для источников данных об оборудовании.
    """
    def get_machine_tool(self, model_name: str) -> MachineTool:
        """
        Получает данные об оборудовании по модели.
        
        Args:
            model_name: Имя модели оборудования
            
        Returns:
            Объект с данными об оборудовании
        """
        pass


class DatabaseMachineToolSource:
    """
    Источник данных об оборудовании из базы данных.
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


class DefaultMachineToolSource:
    """
    Источник данных об оборудовании по умолчанию.
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
            return MachineTool.construct(
                model="DMG CTX beta 2000",
                length=Decimal("6234"),
                width=Decimal("3210"),
                height=Decimal("2052"),
                automation="Автоматическая",
                weight=Decimal(10000.0),
                power_consumption=Decimal(35.0),
            )
        raise ValueError(f"Модель {model_name} не поддерживается")
