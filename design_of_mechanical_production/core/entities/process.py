#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List

from design_of_mechanical_production.core.entities import MachineInfo
from design_of_mechanical_production.core.interfaces import IMachineInfo, IOperation, IProcess
from design_of_mechanical_production.settings import get_setting


@dataclass
class Process(IProcess):
    """
    Класс, представляющий технологический процесс.
    """

    operations: List[IOperation] = field(default_factory=list)
    _machines: Dict[str, IMachineInfo] = field(default_factory=dict)

    def calculate_required_machines(
        self,
        production_volume: float,
        fund_of_working: int = int(get_setting('fund_of_working')),
        kv: Decimal = Decimal(str(get_setting('kv'))),
        kp: Decimal = Decimal(str(get_setting('kp'))),
    ) -> None:
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
            operation.calculated_equipment_count = num_mach
            operation.accept_count(num_mach)
            if operation.equipment.model not in machines:
                machines[operation.equipment.model] = MachineInfo(
                    model=operation.equipment, calculated_count=Decimal('0')
                )
            machines[operation.equipment.model].calculated_count += num_mach
        self._machines = machines

    @property
    def machines(self) -> Dict[str, IMachineInfo]:
        """
        Количество станков по типам.
        """
        return self._machines

    @property
    def accepted_machines_count(self) -> int:
        """
        Общее количество станков.
        """
        return sum(op.accepted_equipment_count for op in self.operations)

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков.
        """
        return sum(op.calculated_equipment_count for op in self.operations)

    @property
    def total_time(self) -> Decimal:
        """
        Общее время на выполнение всех операций.
        """
        return sum(op.time for op in self.operations)

    @property
    def average_load_factor(self) -> Decimal:
        """
        Средний коэффициент загрузки станков.
        """
        return sum(op.load_factor for op in self.operations) / len(self.operations) if self.operations else Decimal('0')

    def calculate_percentage(self) -> None:
        """
        Рассчитывает долю от общей трудоемкости для каждой операции.
        """
        for operation in self.operations:
            operation.calculate_percentage(self.total_time)

    def add_operation(self, operation: IOperation) -> None:
        """
        Добавляет операцию в процесс.

        Args:
            operation: Операция для добавления
        """
        self.operations.append(operation)
        self.calculate_percentage()
