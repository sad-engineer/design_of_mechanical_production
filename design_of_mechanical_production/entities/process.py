#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import List, Dict
from decimal import Decimal

from design_of_mechanical_production.entities.operation import Operation
from design_of_mechanical_production.entities.workshop_zone import MachineInfo
from design_of_mechanical_production.settings import get_setting


@dataclass
class Process:
    """
    Класс, представляющий технологический процесс.
    """
    operations: List[Operation]  # Список операций
    total_time: Decimal = Decimal('0')

    def calculate_required_machines(self,
                                    production_volume: int,
                                    fund_of_working: int = int(get_setting('fund_of_working')),
                                    kv: Decimal = Decimal(str(get_setting('kv'))),
                                    kp: Decimal = Decimal(str(get_setting('kp'))),
                                    ) -> Dict[str, MachineInfo]:
        """
        Рассчитывает необходимое количество станков по формуле:
        num_mach = complexity_norm/(fund_of_working * kv * kp)

        Args:
            production_volume: Годовой объем производства
            fund_of_working: Действительный фонд времени работы одного станка, ч
            kv: Коэффициент выполнения норм
            kp: Коэффициент прогрессивности технологии

        Returns:
            Словарь, где ключ - модель станка, значение - необходимое количество
        """
        for operation in self.operations:
            complexity_norm = Decimal(production_volume) * operation.time
            num_mach = complexity_norm / (Decimal(fund_of_working) * kv * kp)
            operation.calculated_machines_count = num_mach
            operation.accept_machines_count()
        return self.machines_count

    @property
    def machines_count(self) -> Dict[str, MachineInfo]:
        """
        Количество станков по типам.
        """
        count = {}
        for operation in self.operations:
            if operation.equipment.model not in count:
                count[operation.equipment.model] = MachineInfo(
                    model=operation.equipment,
                    calculated_count=operation.calculated_machines_count
                )
            else:
                calculated_count = count[operation.equipment.model].calculated_count
                calculated_count += operation.calculated_machines_count
                count[operation.equipment.model] = MachineInfo(
                    model=operation.equipment,
                    calculated_count=calculated_count
                )
        return count
    
    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков.
        """
        return sum(op.accepted_machines_count for op in self.operations)
    
    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков.
        """
        return sum(op.calculated_machines_count for op in self.operations)
    
    def calculate_total_time(self) -> Decimal:
        """
        Общее время на выполнение всех операций.
        """
        self.total_time = sum(op.time for op in self.operations)

    @property
    def average_load_factor(self) -> Decimal:
        """
        Средний коэффициент загрузки станков.
        """
        sum_calculated_machines_count = sum(op.calculated_machines_count for op in self.operations)
        sum_accepted_machines_count = sum(op.accepted_machines_count for op in self.operations)
        return sum_calculated_machines_count/sum_accepted_machines_count
    
    def calculate_percentage(self) -> None:
        """
        Рассчитывает долю от общей трудоемкости для каждой операции.
        """
        self.calculate_total_time()
        for operation in self.operations:
            operation.percentage = (operation.time / self.total_time) * 100
            
