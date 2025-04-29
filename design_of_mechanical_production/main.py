#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
from pathlib import Path
from typing import List
from decimal import Decimal

from design_of_mechanical_production.entities import (
    Workshop,
    Operation,
    Process,
    EquipmentFactory
)
from design_of_mechanical_production.inputdata import ExcelReader, create_initial_data
from design_of_mechanical_production.output import TextReportGenerator
from design_of_mechanical_production.settings.manager import get_setting, set_setting


def create_workshop_from_data(parameters_data: dict, process_data: List[dict]) -> Workshop:
    """
    Создает объект цеха из входных данных.
    """
    # Создаем фабрику оборудования
    equipment_factory = EquipmentFactory()
    
    # Создаем список операций
    operations = []
    for op_data in process_data:
        equipment = equipment_factory.create_equipment(op_data['machine'])
        operation = Operation(
            number=op_data['number'],
            name=op_data['name'],
            time=Decimal(str(op_data['time'])),
            equipment=equipment
        )
        operations.append(operation)
    
    # Создаем технологический процесс
    process = Process(operations=operations)
    process.calculate_percentage()

    # Создаем цех
    workshop = Workshop(
        name=parameters_data['name'],
        production_volume=int(parameters_data['production_volume']),
        mass_detail=Decimal(str(parameters_data['mass_detail'])),
        process=process
    )
    
    # Рассчитываем требуемую площадь
    workshop.calculate_required_area()
    workshop.calculate_total_area()

    return workshop


def ensure_directories_exist():
    """
    Создает необходимые директории, если они не существуют.
    """
    # Создаем директории для входных и выходных данных
    input_dir = Path(get_setting('input_data_path')).parent
    output_dir = Path(get_setting('report_path')).parent
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)


def main():
    # Создаем необходимые директории
    ensure_directories_exist()
    
    # Проверяем существование файла с начальными данными
    initial_data_file = Path(get_setting('input_data_path'))
    if not os.path.exists(initial_data_file):
        print("Файл с начальными данными не найден. Создаем новый файл...")
        create_initial_data()
        print("Файл с начальными данными успешно создан.")

    # Чтение данных
    reader = ExcelReader(initial_data_file)
    parameters_data = reader.read_parameters_data()
    process_data = reader.read_process_data()

    # Создание объекта цеха
    workshop = create_workshop_from_data(parameters_data, process_data)

    # Генерация и сохранение отчета
    report_generator = TextReportGenerator()
    report = report_generator.generate_report(workshop)

    report_path = Path(get_setting('report_path'))
    if report_generator.save_report(report, report_path):
        print("Отчет успешно сгенерирован и сохранен в output/report.txt")
    else:
        print("Ошибка при сохранении отчета")


if __name__ == "__main__":
    main()
