#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from decimal import Decimal
from math import ceil

from design_of_mechanical_production.domain.entities.equipment import Equipment


@dataclass
class Operation:
    """
    Класс, представляющий технологическую операцию.
    """
    number: str                                         # Номер операции
    name: str                                           # Название операции
    time: Decimal                                       # Норма времени на операцию
    equipment: Equipment                                # Модель станка
    calculated_machines_count: Decimal = Decimal('0')   # Расчетное количество станков
    accepted_machines_count: int = 0                    # Принятое количество станков (округленное вверх)
    load_factor: Decimal = Decimal('0')                 # Коэффициент загрузки станков
    
    def accept_machines_count(self) -> None:
        """
        Округляет расчетное количество станков вверх до целого числа
        и пересчитывает коэффициент загрузки.
        """
        self.accepted_machines_count = ceil(self.calculated_machines_count)
        self.calculate_load_factor()
        
    def calculate_load_factor(self) -> None:
        """
        Рассчитывает коэффициент загрузки станков по формуле:
        К_З = С_Р / С_ПР
        где:
        С_Р - расчетное количество станков
        С_ПР - принятое количество станков
        """
        if self.accepted_machines_count > 0:
            self.load_factor = self.calculated_machines_count / Decimal(self.accepted_machines_count)
        else:
            self.load_factor = Decimal('0')
        