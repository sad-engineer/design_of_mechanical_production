#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List

from design_of_mechanical_production.core.entities.machine_info import MachineInfo
from design_of_mechanical_production.core.entities.operation import Operation
from design_of_mechanical_production.core.entities.types import IMachineInfo, IOperation, IProcess
from design_of_mechanical_production.settings.manager import get_setting


@dataclass
class Process(IProcess):
    """
    Класс, представляющий технологический процесс.
    """

    operations: List[IOperation] = field(default_factory=list)
    total_time: Decimal = Decimal('0')

    def calculate_required_machines(
        self,
        production_volume: float,
        fund_of_working: int = int(get_setting('fund_of_working')),
        kv: Decimal = Decimal(str(get_setting('kv'))),
        kp: Decimal = Decimal(str(get_setting('kp'))),
    ) -> Dict[str, IMachineInfo]:
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
        machines: Dict[str, IMachineInfo] = {}
        for operation in self.operations:
            complexity_norm = Decimal(production_volume) * operation.time
            num_mach = complexity_norm / (Decimal(fund_of_working) * kv * kp)
            operation.calculated_machines_count = num_mach
            operation.accept_machines_count()
            if operation.equipment.model not in machines:
                machines[operation.equipment.model] = MachineInfo(model=operation.equipment, calculated_count=Decimal('0'))
            machines[operation.equipment.model].calculated_count += num_mach
        return machines

    @property
    def machines_count(self) -> Dict[str, IMachineInfo]:
        """
        Количество станков по типам.
        """
        return self.calculate_required_machines(0)

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

    def calculate_total_time(self) -> None:
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
        return sum_calculated_machines_count / sum_accepted_machines_count

    def calculate_percentage(self) -> None:
        """
        Рассчитывает долю от общей трудоемкости для каждой операции.
        """
        self.calculate_total_time()
        for operation in self.operations:
            operation.percentage = (operation.time / self.total_time) * 100

    def add_operation(self, operation: Operation) -> None:
        """
        Добавляет операцию в процесс.

        Args:
            operation: Операция для добавления
        """
        self.operations.append(operation)
