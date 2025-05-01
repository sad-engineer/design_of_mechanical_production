#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional

from design_of_mechanical_production.core.entities.equipment import Equipment
from design_of_mechanical_production.core.entities.machine_tool_source import DatabaseMachineToolSource, DefaultMachineToolSource, MachineToolSource
from design_of_mechanical_production.core.entities.types import IEquipment, IEquipmentFactory


class EquipmentFactory(IEquipmentFactory):
    """
    Фабрика для создания оборудования.
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
        self._equipment_cache: Dict[str, IEquipment] = {}

    def create_equipment(self, model: str) -> IEquipment:
        """
        Создает оборудование по модели.

        Args:
            model: Модель оборудования

        Returns:
            IEquipment: Созданное оборудование
        """
        if model in self._equipment_cache:
            return self._equipment_cache[model]

        try:
            machine_tool = self.source.get_machine_tool(model)
        except (TypeError, ValueError):
            try:
                machine_tool = self.default_source.get_machine_tool(model)
            except ValueError as e:
                raise ValueError(f"Не удалось создать оборудование: {str(e)}")

        try:
            equipment = Equipment(
                name=None,
                model=model,
                length=Decimal(str(machine_tool.length)) / 1000,
                width=Decimal(str(machine_tool.width)) / 1000,
                height=Decimal(str(machine_tool.height)) / 1000,
                automation=machine_tool.automation,
                weight=machine_tool.weight,
                power_consumption=Decimal(str(machine_tool.power_lathe_passport_kvt)),
            )
        except AttributeError:
            print(machine_tool)

        self._equipment_cache[model] = equipment
        return equipment
