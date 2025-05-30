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

FUND_OF_WORKING = float(get_setting('fund_of_working'))
KV = Decimal(str(get_setting('kv')))
KP = Decimal(str(get_setting('kp')))


@dataclass
class Process(IProcess):
    """
    Класс, представляющий технологический процесс.
    """

    operations: List[IOperation] = field(default_factory=list)
    _compliance_coefficient: Decimal = KV
    _progressivity_coefficient: Decimal = KP
    _fund_of_working: Decimal = FUND_OF_WORKING
    _machines: Dict[str, IMachineInfo] = field(default_factory=dict)

    def calculate_required_machines(self) -> None:
        """
        Рассчитывает необходимое количество станков по формуле:
        num_mach = operation.time/(fund_of_working * compliance_coefficient * progressivity_coefficient)
        """
        machines: Dict[str, IMachineInfo] = {}
        for operation in self.operations:
            operation.fund_of_working = self.fund_of_working
            operation.compliance_coefficient = self.compliance_coefficient
            operation.progressivity_coefficient = self.progressivity_coefficient
            time = Decimal(str(operation.time))
            num_mach = time / (
                Decimal(self.fund_of_working) * self.compliance_coefficient * self.progressivity_coefficient
            )
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

    @property
    def fund_of_working(self) -> Decimal:
        """
        Действительный фонд времени работы одного станка, ч
        """
        return self._fund_of_working

    @fund_of_working.setter
    def fund_of_working(self, value: Decimal) -> None:
        """
        Устанавливает действительный фонд времени работы одного станка, ч
        """
        self._fund_of_working = value
        self.calculate_required_machines()

    @property
    def compliance_coefficient(self) -> Decimal:
        """
        Коэффициент выполнения нормы.
        """
        return self._compliance_coefficient

    @compliance_coefficient.setter
    def compliance_coefficient(self, value: Decimal) -> None:
        """
        Устанавливает коэффициент выполнения нормы.
        """
        self._compliance_coefficient = value
        self.calculate_required_machines()
    
    @property
    def progressivity_coefficient(self) -> Decimal:
        """
        Коэффициент прогрессивности.
        """
        return self._progressivity_coefficient  
    
    @progressivity_coefficient.setter
    def progressivity_coefficient(self, value: Decimal) -> None:
        """
        Устанавливает коэффициент прогрессивности.
        """
        self._progressivity_coefficient = value
        self.calculate_required_machines()
