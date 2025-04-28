#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from decimal import Decimal

from machine_tools import MachineToolsContainer as Container
from machine_tools import MachineTool


def get_machine_tool_from_db(model: str):
    # Создаем креатор
    creator = Container().creator()
    # Получение параметров станка по имени
    return creator.by_name(model)


@dataclass
class Equipment:
    """
    Класс, представляющий оборудование в цехе.
    """
    model: str
    length: Decimal
    width: Decimal
    height: Decimal
    automation: str
    weight: Decimal
    power_consumption: Decimal

    def __init__(self, model: str):
        self.model = model
        try:
            machine_tool = get_machine_tool_from_db(model)
        except TypeError:
            machine_tool = get_default_machine_tool(self)
        self.length = Decimal(str(machine_tool.length)) / 1000
        self.width = Decimal(str(machine_tool.width)) / 1000
        self.height = Decimal(str(machine_tool.height)) / 1000
        self.automation = machine_tool.automation
        self.weight = machine_tool.weight
        self.power_consumption = machine_tool.power_lathe_passport_kvt

    @property
    def area(self):
        return self.length * self.width


def get_default_machine_tool(equipment: Equipment) -> Equipment:
    
    if equipment.model == "DMG CTX beta 2000":
        return MachineTool.construct(
            model="DMG CTX beta 2000",
            length=Decimal("6234"),
            width=Decimal("3210"),
            height=Decimal("2052"),
            automation="Автоматическая",
            weight=Decimal(10000.0),
            power_consumption=Decimal(35.0),
        )
    