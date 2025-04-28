#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import Optional

from design_of_mechanical_production.entities.equipment import Equipment
from design_of_mechanical_production.entities.machine_tool_source import (
    MachineToolSource,
    DatabaseMachineToolSource,
    DefaultMachineToolSource
)


class EquipmentFactory:
    """
    Фабрика для создания объектов оборудования.
    """
    def __init__(self, source: Optional[MachineToolSource] = None):
        """
        Инициализирует фабрику с указанным источником данных.
        
        Args:
            source: Источник данных об оборудовании. Если не указан, используется комбинация
                   DatabaseMachineToolSource и DefaultMachineToolSource
        """
        self.source = source or DatabaseMachineToolSource()
        self.default_source = DefaultMachineToolSource()

    def create_equipment(self, model: str) -> Equipment:
        """
        Создает объект оборудования по указанной модели.
        
        Args:
            model: Модель оборудования
            
        Returns:
            Объект оборудования
            
        Raises:
            ValueError: Если не удалось создать оборудование
        """
        try:
            machine_tool = self.source.get_machine_tool(model)
        except (TypeError, ValueError):
            try:
                machine_tool = self.default_source.get_machine_tool(model)
            except ValueError as e:
                raise ValueError(f"Не удалось создать оборудование: {str(e)}")

        return Equipment(
            model=model,
            length=Decimal(str(machine_tool.length)) / 1000,
            width=Decimal(str(machine_tool.width)) / 1000,
            height=Decimal(str(machine_tool.height)) / 1000,
            automation=machine_tool.automation,
            weight=machine_tool.weight,
            power_consumption=machine_tool.power_lathe_passport_kvt
        )
