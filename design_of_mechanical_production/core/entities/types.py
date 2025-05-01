#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from __future__ import annotations

from decimal import Decimal
from typing import Dict, List, Optional, Protocol, TypeVar, Union


class IAreaCalculator(Protocol):
    """
    Интерфейс для калькуляторов площади.
    """

    def calculate_area(self, machines: Dict[str, 'IMachineInfo']) -> Decimal:
        """
        Рассчитывает площадь зоны.

        Args:
            machines: Словарь с информацией о станках

        Returns:
            Decimal: Рассчитанная площадь
        """
        ...


class IProcess(Protocol):
    """
    Интерфейс для технологического процесса.
    """

    operations: List['IOperation']
    total_time: Decimal

    def calculate_required_machines(self, production_volume: float) -> Dict[str, 'IMachineInfo']:
        """
        Рассчитывает необходимое количество станков.

        Args:
            production_volume: Объем производства

        Returns:
            Dict[str, IMachineInfo]: Словарь с информацией о станках
        """
        ...

    @property
    def machines_count(self) -> Dict[str, IMachineInfo]:
        """
        Количество станков по типам.
        """
        ...

    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков.
        """
        return ...

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков.
        """
        return ...

    def calculate_total_time(self) -> None:
        """
        Общее время на выполнение всех операций.
        """
        ...

    @property
    def average_load_factor(self) -> Decimal:
        """
        Средний коэффициент загрузки станков.
        """
        ...

    def calculate_percentage(self) -> None:
        """
        Рассчитывает долю от общей трудоемкости для каждой операции.
        """
        ...

    def add_operation(self, operation: 'IOperation') -> None:
        """
        Добавляет операцию в процесс.

        Args:
            operation: Операция для добавления
        """
        ...


class IOperation(Protocol):
    """
    Интерфейс для операции.
    """

    number: int
    name: str
    time: Decimal
    equipment: 'IEquipment'
    calculated_machines_count: Decimal  # Расчетное количество станков
    accepted_machines_count: int  # Принятое количество станков (округленное вверх)
    load_factor: Decimal  # Коэффициент загрузки станков
    percentage: Optional[Decimal]

    def accept_machines_count(self) -> None:
        """
        Округляет количество станков до целого числа.
        """
        ...

    def calculate_load_factor(self) -> None:
        """
        Рассчитывает коэффициент загрузки станков.
        """
        ...

    def calculate_percentage(self, total_time: Decimal) -> None:
        """
        Рассчитывает процентное соотношение операции.

        Args:
            total_time: Общее время процесса
        """
        ...


class IWorkshop(Protocol):
    """
    Интерфейс для цеха.
    """

    name: str
    production_volume: float
    mass_detail: Decimal
    process: IProcess
    equipment_list: List[IEquipment]
    zones: Dict[str, IWorkshopZone]
    total_area: Decimal
    required_area: Decimal
    length: Decimal

    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков в цехе.
        """
        ...

    def calculate_total_area(self) -> Decimal:
        """
        Рассчитывает общую площадь цеха.
        """
        ...

    def calculate_required_area(self) -> Decimal:
        """
        Рассчитывает общую площадь, занимаемую оборудованием.
        """
        ...

    def add_equipment(self, equipment: IEquipment) -> None:
        """
        Добавляет оборудование в цех.
        """
        ...

    def get_equipment_count(self) -> Dict[str, IMachineInfo]:
        """
        Возвращает количество оборудования.
        """
        ...

    def get_machines_count(self) -> Dict[str, int]:
        """
        Возвращает количество станков.
        """
        ...

    def add_zone(self, name: str, zone: IWorkshopZone) -> None:
        """
        Добавляет зону в цех.

        Args:
            name: Название зоны
            zone: Объект зоны
        """
        ...


class IWorkshopZone(Protocol):
    """
    Интерфейс для зоны цеха.
    """

    name: str
    machines: Dict[str, 'IMachineInfo']

    def calculate_area(self) -> Decimal:
        """
        Рассчитывает площадь зоны.
        """
        ...

    def add_machine(self, name: str, machine: IMachineInfo) -> None:
        """
        Добавляет станок в зону.

        Args:
            name: Название станка
            machine: Информация о станке
        """
        ...

    @property
    def calculated_machines_count(self) -> Decimal:
        """
        Общее расчетное количество станков в зоне.
        """
        ...

    @property
    def accepted_machines_count(self) -> int:
        """
        Возвращает количество станков в зоне.
        """
        ...

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь зоны.
        """
        ...


class IEquipment(Protocol):
    """
    Интерфейс для оборудования.
    """

    name: str
    model: str
    length: Decimal
    width: Decimal
    height: Decimal
    automation: str
    weight: Decimal
    power_consumption: Decimal

    @property
    def area(self) -> Decimal:
        """
        Возвращает площадь, занимаемую оборудованием.
        """
        return Decimal("0")

    @property
    def power(self) -> Decimal:
        """
        Возвращает потребляемую мощность оборудования.
        """
        return Decimal("0")

    @property
    def dimensions(self) -> Dict[str, Decimal]:
        """
        Возвращает габаритные размеры оборудования.
        """
        return {"length": self.length, "width": self.width, "height": self.height}


class IEquipmentFactory(Protocol):
    """
    Интерфейс для фабрики оборудования.
    """

    def create_equipment(self, model: str) -> IEquipment:
        """
        Создает оборудование по модели.

        Args:
            model: Модель оборудования

        Returns:
            IEquipment: Созданное оборудование
        """
        ...


class IMachineInfo(Protocol):
    """
    Интерфейс для информации о станке в зоне.

    Attributes:
        model: Название станка или объект оборудования
        calculated_count: Расчетное количество станков
        actual_count: Фактическое количество станков (может быть None)
    """

    model: Union[str, 'IEquipment']
    calculated_count: Decimal
    actual_count: Optional[int]

    @property
    def accepted_count(self) -> int:
        """
        Возвращает принятое количество станков (округленное вверх).

        Returns:
            int: Принятое количество станков
        """
        ...

    def __post_init__(self) -> None:
        """
        Инициализирует фактическое количество станков после создания объекта.
        """
        ...


# Базовые типы
T = TypeVar('T')
DecimalType = Union[Decimal, float, int, str]
AreaCalculatorType = Union['AreaCalculator', 'SpecificAreaCalculator']
WorkshopZoneType = Union['WorkshopZone', 'SpecificWorkshopZone']

# Типы для данных
MachineCountType = Dict[str, 'IMachineInfo']
EquipmentListType = List['IEquipment']
ZoneDictType = Dict[str, IWorkshopZone]
ProcessType = IProcess
OperationType = IOperation
WorkshopType = IWorkshop
EquipmentType = IEquipment
EquipmentFactoryType = IEquipmentFactory
MachineInfoType = IMachineInfo

# Типы для конфигурации
ConfigType = Dict[str, Union[DecimalType, str, bool]]
SettingType = Union[DecimalType, str, bool, Dict[str, DecimalType]]

# Типы для ввода/вывода
ReportType = Dict[str, Union[str, DecimalType, List[str]]]
InputDataType = Dict[str, Union[str, int, float, List[Dict[str, Union[str, float]]]]]
