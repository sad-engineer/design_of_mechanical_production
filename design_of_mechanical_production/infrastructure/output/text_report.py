#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import List
from decimal import Decimal
from design_of_mechanical_production.application.interfaces.report_generator import ReportGenerator
from design_of_mechanical_production.domain.entities.workshop import Workshop
from design_of_mechanical_production.domain.entities.equipment import Equipment
from design_of_mechanical_production.domain.entities.worker import Worker
from design_of_mechanical_production.domain.services.workshop_calculator import WorkshopCalculator


class TextReportGenerator(ReportGenerator):
    """
    Класс для генерации текстовых отчетов.
    """
    
    def generate_report(self, workshop: Workshop) -> str:
        """
        Генерирует текстовый отчет о цехе.
        """
        calculator = WorkshopCalculator()
        
        report = []
        report.append(f"Отчет по цеху: {workshop.name}")
        report.append("=" * 50)
        
        # Общая информация
        report.append("\n1. Общая информация:")
        report.append(f"Годовой объем производства: {workshop.production_volume} шт.")
        report.append(f"Общая площадь цеха: {workshop.total_area} м²")
        report.append(f"Требуемая площадь: {workshop.calculate_required_area()} м²")
        
        # Информация об оборудовании
        report.append("\n2. Оборудование:")
        equipment_details = workshop.get_equipment_details()
        for detail in equipment_details:
            report.append(f"\n- {detail['name']} ({detail['model']}):")
            report.append(f"  Количество: {detail['required_count']} шт.")
            report.append(f"  Площадь на единицу: {workshop.equipment_list[0].area} м²")
            report.append(f"  Общая площадь: {detail['total_area']} м²")
            report.append(f"  Потребляемая мощность на единицу: {workshop.equipment_list[0].power_consumption} кВт")
            report.append(f"  Общая потребляемая мощность: {detail['total_power']} кВт")
            report.append(f"  Количество рабочих на единицу: {workshop.equipment_list[0].worker_count}")
            report.append(f"  Общее количество рабочих: {detail['total_workers']}")
        
        # Информация о рабочих
        report.append("\n3. Персонал:")
        total_workers = calculator.calculate_required_workers(workshop.equipment_list, workshop.production_volume)
        report.append(f"Общее количество рабочих: {total_workers}")
        
        # Экономические показатели
        report.append("\n4. Экономические показатели:")
        total_power = calculator.calculate_total_power_consumption(workshop.equipment_list)
        report.append(f"Годовое потребление электроэнергии: {total_power} кВт*ч")
        
        # Эффективность
        report.append("\n5. Показатели эффективности:")
        efficiency = calculator.calculate_workshop_efficiency(workshop)
        report.append(f"Общая эффективность цеха: {efficiency:.2%}")
        
        return "\n".join(report)
    
    def save_report(self, report: str, filepath: str) -> bool:
        """
        Сохраняет отчет в текстовый файл.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении отчета: {str(e)}")
            return False
