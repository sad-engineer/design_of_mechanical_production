#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
from decimal import Decimal
from domain.entities.workshop import Workshop
from domain.entities.equipment import Equipment
from domain.entities.worker import Worker
from domain.entities.operation import Operation
from domain.entities.process import Process
from infrastructure.input.excel_reader import ExcelReader
from infrastructure.output.text_report import TextReportGenerator
from domain.services.workshop_calculator import WorkshopCalculator
from inputdata.create_initial_data import create_initial_data


def create_workshop_from_data(parameters_data: dict, worker_data: list, process_data: list) -> Workshop:
    """
    Создает объект цеха из входных данных.
    """
    # Создаем список рабочих
    workers_list = []
    for wr_data in worker_data:
        worker = Worker(
            name=wr_data['name'],
            position=wr_data['position'],
            qualification=int(wr_data['qualification']),
            hourly_rate=Decimal(str(wr_data['hourly_rate']))
        )
        workers_list.append(worker)
    
    # Создаем список операций
    operations = []
    for op_data in process_data:
        equipment = Equipment(
            model=op_data['machine'],
        )
        operation = Operation(
            number=op_data['number'],
            name=op_data['name'],
            time=Decimal(str(op_data['time'])),
            equipment=equipment
        )
        operations.append(operation)
    
    # Создаем технологический процесс
    process = Process(operations=operations)
    
    # Создаем цех
    workshop = Workshop(
        name=parameters_data['name'],
        total_area=Decimal('0'),  # Будет рассчитано позже
        production_volume=int(parameters_data['production_volume']),
        workers_list=workers_list,
        mass_detail=Decimal(str(parameters_data['mass_detail'])),
        process=process
    )
    
    # Рассчитываем требуемую площадь
    required_area = workshop.calculate_required_area()
    workshop.total_area = required_area
    
    return workshop


def main():
    # Проверяем существование файла с начальными данными
    initial_data_file = 'inputdata/initial_data.xlsx'
    if not os.path.exists(initial_data_file):
        print("Файл с начальными данными не найден. Создаем новый файл...")
        create_initial_data()
        print("Файл с начальными данными успешно создан.")

    # Чтение данных
    reader = ExcelReader(initial_data_file)
    parameters_data = reader.read_parameters_data()
    worker_data = reader.read_worker_data()
    process_data = reader.read_process_data()

    # Создание объекта цеха
    workshop = create_workshop_from_data(parameters_data, worker_data, process_data)

    # Генерация и сохранение отчета
    report_generator = TextReportGenerator()
    report = report_generator.generate_report(workshop)

    if report_generator.save_report(report, 'output/report.txt'):
        print("Отчет успешно сгенерирован и сохранен в output/report.txt")
    else:
        print("Ошибка при сохранении отчета")


if __name__ == "__main__":
    main()
