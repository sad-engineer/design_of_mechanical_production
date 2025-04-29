#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Union
from decimal import Decimal
from math import ceil

from design_of_mechanical_production.entities.equipment import Equipment


@dataclass
class MachineInfo:
    """
    Класс для хранения информации о станке в зоне.
    """
    model: Union[Equipment, str]    # Название станка
    calculated_count: Decimal       # Расчетное количество станков
    accepted_count: int             # Принятое количество станков (округленное вверх)
    
    def __init__(self, model: Union[Equipment, str], calculated_count: Decimal):
        self.model = model
        self.calculated_count = calculated_count
        self.accepted_count = ceil(calculated_count) 
        