#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Optional, Union

from design_of_mechanical_production.core.entities import AreaCalculator, SpecificAreaCalculator
from design_of_mechanical_production.core.interfaces import (
    IAreaCalculator,
    IMachineInfo,
    ISpecificWorkshopZone,
    IWorkshopZone,
)
from design_of_mechanical_production.settings import get_setting


class BaseWorkshopZone(ABC):
    """
    Абстрактный базовый класс для всех типов зон цеха.
    """

    name: str  # Название зоны
    # __tokens - Признаки сортировки, поле задается фабрикой
    __tokens: Dict[str, str] = field(default_factory=lambda: {"group": "main"})

    @property
    @abstractmethod
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        pass

    @property
    @abstractmethod
    def tokens(self) -> Dict[str, str]:
        """
        Возвращает признаки сортировки.
        """
        pass

    @abstractmethod
    def set_tokens(self, tokens: Dict[str, str]) -> None:
        """
        Устанавливает признаки сортировки.
        """
        pass


@dataclass
class WorkshopZone(IWorkshopZone, BaseWorkshopZone):
    """
    Класс, представляющий зону цеха.
    """

    name: str
    machines: Dict[str, IMachineInfo] = field(default_factory=dict)
    _area_calculator: Optional[IAreaCalculator] = None
    # __tokens - Признаки сортировки, поле задается фабрикой
    __tokens: Dict[str, str] = field(default_factory=lambda: {"group": "main"})

    def __post_init__(self) -> None:
        """
        Инициализирует калькулятор площади после создания объекта.
        """
        if self._area_calculator is None:
            self._area_calculator = AreaCalculator(Decimal(get_setting("passage_area")))

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        return self._area_calculator.calculate_area(self.machines)

    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        self.machines[name] = machine

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков в зоне.
        """
        return sum(machine.calculated_count for machine in self.machines.values())

    @property
    def accepted_machines_count(self) -> int:
        """
        Возвращает количество станков в зоне.
        """
        return sum(machine.accepted_count for machine in self.machines.values())

    def set_tokens(self, tokens: Dict[str, str]) -> None:
        """
        Устанавливает признаки сортировки.
        """
        self.__tokens = tokens

    @property
    def tokens(self) -> Dict[str, str]:
        """
        Возвращает признаки сортировки.
        """
        return self.__tokens


@dataclass
class SpecificWorkshopZone(ISpecificWorkshopZone, BaseWorkshopZone):
    """
    Класс, представляющий вспомогательную зону цеха.
    Площадь определяется по удельной площади в пересчете на количество элементов.
    """

    name: str  # Название зоны
    specific_area: Decimal  # удельная площадь зоны в м²
    unit_of_calculation: Union[int, Decimal, float] = 0  # количество элементов в зоне для расчета площади
    _area_calculator: IAreaCalculator = None  # Калькулятор площади
    # __tokens - Признаки сортировки, поле задается фабрикой
    __tokens: Dict[str, str] = field(default_factory=lambda: {"group": "additional"})

    def __post_init__(self) -> None:
        """
        Инициализирует калькулятор площади после создания объекта.
        """
        if self._area_calculator is None:
            self._area_calculator = SpecificAreaCalculator(self.specific_area, self.unit_of_calculation)

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        return self._area_calculator.calculate_area({})

    def set_tokens(self, tokens: Dict[str, str]) -> None:
        """
        Устанавливает признаки сортировки.
        """
        self.__tokens = tokens

    @property
    def tokens(self) -> Dict[str, str]:
        """
        Возвращает признаки сортировки.
        """
        return self.__tokens
