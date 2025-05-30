#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from sys import exit

from machine_tools import Finder, ListMachineInfoFormatter, ListNameFormatter, MachineInfo

from design_of_mechanical_production.core.entities import Equipment
from design_of_mechanical_production.core.interfaces import IEquipment, IEquipmentFactory


class EquipmentFactory(IEquipmentFactory):
    """
    Фабрика для создания оборудования.
    """

    def create_equipment(self, model: str) -> IEquipment:
        """
        Создает оборудование по модели.

        Args:
            model: Модель оборудования

        Returns:
            IEquipment: Созданное оборудование
        """
        with Finder(limit=None) as finder:
            all_machine_tool = finder.find_all()
            finder._builder.reset_builder()
            finder.set_formatter(ListMachineInfoFormatter())
            machine_tool: MachineInfo = finder.find_by_name(model, exact_match=True)[0]

        if not machine_tool:
            print(
                f"\nСтанок {model} не найден в базе данных."
                f"\nВнесите данные по станку в базу и повторите расчет."
                f"\nИли выберите станок, данные которого содержатся в базе."
                f"\n"
                f"\nДоступные станки:"
                f"\n{chr(10).join(', '.join(all_machine_tool[i:i+50]) for i in range(0, len(all_machine_tool), 200))}"
            )
            exit(1)

        equipment = None
        try:
            equipment = Equipment(
                name=None,
                model=model,
                length=Decimal(str(machine_tool.dimensions.length)) / 1000,
                width=Decimal(str(machine_tool.dimensions.width)) / 1000,
                height=Decimal(str(machine_tool.dimensions.height)) / 1000,
                automation=machine_tool.automation.value,
                weight=machine_tool.weight,
                power_consumption=Decimal(str(machine_tool.power)),
            )
        except AttributeError:
            print(machine_tool)

        return equipment
