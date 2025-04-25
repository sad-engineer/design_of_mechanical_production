#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from typing import List, Dict
from decimal import Decimal

from design_of_mechanical_production.domain.entities.equipment import Equipment
from design_of_mechanical_production.domain.entities.worker import Worker
from design_of_mechanical_production.domain.entities.process import Process
from design_of_mechanical_production.domain.entities.workshop_zone import (
    WorkshopZone,
    MachineInfo,
    SpecificWorkshopZone
)
from design_of_mechanical_production.settings import get_setting


@dataclass
class Workshop:
    """
    Класс, представляющий машиностроительный цех.
    """
    name: str
    total_area: Decimal
    production_volume: int
    workers_list: List[Worker]
    mass_detail: Decimal
    process: Process
    equipment_list: List[Equipment] = field(default_factory=list)
    zones: Dict[str, WorkshopZone] = field(default_factory=dict)  # Словарь зон цеха

    @property
    def total_machines_count(self) -> int:
        """
        Общее количество станков в цехе.
        """
        total_count = 0
        for name, zone in self.zones.items():
            total_count += zone.total_machines_count
        return total_count

    def calculate_required_area(self) -> Decimal:
        """
        Рассчитывает требуемую площадь цеха с учетом проходов и проездов.
        """
        equipment_area = self.calculate_total_equipment_area()
        area_coefficient = Decimal(str(get_setting('area_coefficient', '1.7')))
        return equipment_area * area_coefficient

    def calculate_total_equipment_area(self) -> Decimal:
        """
        Рассчитывает общую площадь, занимаемую оборудованием.
        """
        # Получаем необходимое количество станков по техпроцессу
        machines_count = self.process.calculate_required_machines(self.production_volume)

        # Расчет Основной зоны
        main_zone = WorkshopZone(
            name='Основная зона',
            machines=machines_count,
        )
        self.zones['main_zone'] = main_zone

        # Расчет зоны заточного отделения (5% от общего числа станков)
        grinding_zone_percent = Decimal(str(get_setting('grinding_zone_percent')))
        grinding_zone = WorkshopZone(
            name='Заточное отделение',
            machines={
                "Станок универсально-заточной 3В642": MachineInfo(
                    model=Equipment(model="3В642"),
                    calculated_count=self.zones['main_zone'].total_machines_count * grinding_zone_percent
                )
            },
        )
        self.zones['grinding_zone'] = grinding_zone

        # Расчет зоны ремонтное отделение (25% от общего числа станков)
        repair_zone_percent = Decimal(str(get_setting('repair_zone_percent')))
        repair_zone = WorkshopZone(
            name='Ремонтное отделение',
            machines={
                "Станки в ремонте": MachineInfo(
                    model="Станки в ремонте",
                    calculated_count=self.zones['main_zone'].total_machines_count * repair_zone_percent
                )
            },
        )
        self.zones['repair_zone'] = repair_zone
        

        # Расчет вспомогательных зон
        total_machines_count = main_zone.total_machines_count + grinding_zone.total_machines_count + repair_zone.total_machines_count

        # Склад инструмента
        tool_storage_zone = SpecificWorkshopZone(
            name='Склад инструмента',
            specific_area=Decimal(str(get_setting('specific_areas.tool_storage'))),
            total_equipment_count=total_machines_count 
        )
        self.zones['tool_storage_zone'] = tool_storage_zone

        # Склад приспособлений
        equipment_warehouse_zone = SpecificWorkshopZone(
            name='Склад приспособлений',
            specific_area=Decimal(str(get_setting('specific_areas.equipment_warehouse'))),
            total_equipment_count=total_machines_count 
        )
        self.zones['equipment_warehouse_zone'] = equipment_warehouse_zone

        # Склад заготовок
        work_piece_storage_zone = SpecificWorkshopZone(
            name='Склад заготовок',
            specific_area=Decimal(str(get_setting('specific_areas.work_piece_storage'))),
            total_equipment_count=main_zone.area 
        )
        self.zones['work_piece_storage_zone'] = work_piece_storage_zone

        # Отделение контроля
        control_department_zone = SpecificWorkshopZone(
            name='Отделение контроля',
            specific_area=Decimal(str(get_setting('specific_areas.control_department'))),
            total_equipment_count=total_machines_count 
        )
        self.zones['control_department_zone'] = control_department_zone
        
        # Санитарная зона 1
        sanitary_zone = SpecificWorkshopZone(
            name='Санитарная зона 1',
            specific_area=Decimal(str(get_setting('specific_areas.sanitary_zone'))),
            total_equipment_count=2 
        )
        self.zones['sanitary_zone'] = sanitary_zone
        



        # Суммируем площади с учетом количества станков
        total_area = main_zone.area
        total_area += tool_storage_zone.area
        total_area += equipment_warehouse_zone.area 
        total_area += work_piece_storage_zone.area
        total_area += control_department_zone.area
        total_area += sanitary_zone.area

        return total_area

    def add_equipment(self, equipment: Equipment) -> None:
        """
        Добавляет оборудование в цех.
        """
        self.equipment_list.append(equipment)
    
    def add_worker(self, worker: Worker) -> None:
        """
        Добавляет рабочего в цех.
        """
        self.workers_list.append(worker)
    
    def get_equipment_count(self) -> Dict[str, Decimal]:
        """
        Возвращает необходимое количество оборудования по каждому типу станков.
        """
        return self.process.calculate_required_machines(self.production_volume)
    
    def get_workers_count(self) -> int:
        """
        Возвращает количество рабочих в цехе.
        """
        return len(self.workers_list)
    
    def get_equipment_details(self) -> List[dict]:
        """
        Возвращает детальную информацию об оборудовании с учетом необходимого количества.
        """
        details = []
        machines_count = self.process.calculate_required_machines(self.production_volume)
        
        for equipment in self.equipment_list:
            if equipment.model in machines_count:
                required_count = machines_count[equipment.model]
                details.append({
                    'name': equipment.name,
                    'model': equipment.model,
                    'required_count': required_count,
                    'total_area': equipment.area * required_count,
                    'total_power': equipment.power_consumption * required_count,
                    'total_workers': equipment.worker_count * required_count
                })
        
        return details

    def get_machines_count(self) -> Dict[str, int]:
        """
        Количество станков по типам в цехе.
        """
        machines_count = {}
        for zone in self.zones:
            for machine, count in zone.machines.items():
                if machine in machines_count:
                    machines_count[machine] += count
                else:
                    machines_count[machine] = count
        return machines_count
