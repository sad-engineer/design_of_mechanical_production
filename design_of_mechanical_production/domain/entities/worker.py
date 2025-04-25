#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from design_of_mechanical_production.domain.entities.equipment import Equipment


@dataclass
class Worker:
    """
    Класс, представляющий рабочего в цехе.
    """
    name: str
    position: str
    qualification: int  # Разряд рабочего
    hourly_rate: Decimal
    equipment: Optional[Equipment] = None
    
    def calculate_monthly_salary(self, working_hours: int = 168) -> Decimal:
        """
        Рассчитывает месячную зарплату рабочего.
        
        Args:
            working_hours: Количество рабочих часов в месяц
        """
        return self.hourly_rate * Decimal(working_hours)
    
    def assign_to_equipment(self, equipment: 'Equipment') -> None:
        """
        Назначает рабочего на оборудование.
        """
        self.equipment = equipment
