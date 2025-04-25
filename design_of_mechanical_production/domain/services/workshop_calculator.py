#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from typing import List
from design_of_mechanical_production.domain.entities.workshop import Workshop
from design_of_mechanical_production.domain.entities.equipment import Equipment


class WorkshopCalculator:
    """
    Сервис для расчета параметров цеха.
    """
    
    @staticmethod
    def calculate_required_workers(equipment_list: List[Equipment], production_volume: int) -> int:
        """
        Рассчитывает необходимое количество рабочих.
        """
        total_workers = 0
        for equipment in equipment_list:
            required_equipment_count = equipment.calculate_required_count(production_volume)
            total_workers += required_equipment_count * equipment.worker_count
        return total_workers
    
    @staticmethod
    def calculate_total_power_consumption(equipment_list: List[Equipment]) -> Decimal:
        """
        Рассчитывает общее потребление электроэнергии.
        """
        return sum(equipment.calculate_annual_power_consumption() for equipment in equipment_list)
    
    @staticmethod
    def calculate_equipment_utilization(workshop: Workshop) -> Decimal:
        """
        Рассчитывает коэффициент использования оборудования.
        """
        if not workshop.equipment_list:
            return Decimal('0')
        
        total_utilization = sum(equipment.efficiency for equipment in workshop.equipment_list)
        return total_utilization / len(workshop.equipment_list)
    
    @staticmethod
    def calculate_workshop_efficiency(workshop: Workshop) -> Decimal:
        """
        Рассчитывает общую эффективность цеха.
        """
        equipment_utilization = WorkshopCalculator.calculate_equipment_utilization(workshop)
        area_utilization = workshop.calculate_total_equipment_area() / workshop.total_area
        
        return (equipment_utilization + area_utilization) / Decimal('2')
