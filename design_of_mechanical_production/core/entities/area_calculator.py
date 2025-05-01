#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, Union

from design_of_mechanical_production.core.entities.types import IAreaCalculator, IMachineInfo


class AreaCalculator(IAreaCalculator):
    """
    Реализация калькулятора площади для основной зоны цеха.
    """

    def __init__(self, passage_area: Decimal):
        self.passage_area = passage_area

    def calculate_area(self, machines: Dict[str, IMachineInfo]) -> Decimal:
        area = Decimal('0')
        for machine in machines.values():
            if hasattr(machine.model, 'length') and hasattr(machine.model, 'width'):
                length = machine.model.length
                width = machine.model.width
            else:
                length = Decimal('2.000')
                width = Decimal('1.000')
            area += (length * width + self.passage_area) * machine.accepted_count
        return area


class SpecificAreaCalculator(IAreaCalculator):
    """
    Реализация калькулятора площади для вспомогательной зоны цеха.
    """

    def __init__(self, specific_area: Decimal, total_equipment_count: Union[int, Decimal, float]):
        self.specific_area = specific_area
        self.total_equipment_count = total_equipment_count

    def calculate_area(self, machines: Dict[str, IMachineInfo]) -> Decimal:
        return self.specific_area * self.total_equipment_count
