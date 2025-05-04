#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль для запуска приложения в разных режимах.
"""
import json
from pathlib import Path
from typing import Any, Dict

from design_of_mechanical_production.core.services.workshop_creator import create_workshop_from_data
from design_of_mechanical_production.data.input import ExcelReader
from design_of_mechanical_production.data.output import TextReportGenerator
from design_of_mechanical_production.data.utils.file_system import (
    check_initial_data_file,
    create_initial_data_file,
    ensure_directories_exist,
)
from design_of_mechanical_production.settings import get_setting


def load_launch_config() -> Dict[str, Any]:
    """
    Загружает конфигурацию запуска из файла.

    Returns:
        Dict[str, Any]: Конфигурация запуска приложения
    """
    config_path = Path(__file__).parent.parent.parent / 'launch_config.json'
    if not config_path.exists():
        return {'mode': 'gui', 'theme': 'light'}

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_with_gui() -> None:
    """
    Запускает приложение в режиме GUI.
    """
    # Загружаем конфигурацию запуска
    config = load_launch_config()

    # Проверяем наличие необходимых директорий
    ensure_directories_exist()
    # Проверяем наличие файла с начальными данными
    if not check_initial_data_file():
        create_initial_data_file()

    # Импортируем и запускаем приложение
    from design_of_mechanical_production.gui.app import WorkshopDesignApp

    # Запускаем приложение с конфигурацией
    WorkshopDesignApp(config=config).run()


def run_without_gui() -> None:
    """
    Запускает приложение в консольном режиме без графического интерфейса.

    Выполняет следующие действия:
    1. Создает необходимые директории
    2. Проверяет и создает файл с начальными данными (если он не существует).
    В качестве начальных данных используется файл `initial_data.xlsx` в папке `data` корневой директории проекта.
    3. Дает пользователю время для корректировки начальных данных
    4. Читает данные из файла начальных данных
    5. Создает объект цеха, делает расчет площади цеха
    6. Генерирует и сохраняет отчет
    """
    # Создаем необходимые директории
    ensure_directories_exist()

    # Проверяем и создаем файл с начальными данными
    initial_data_file = create_initial_data_file()
    print(f"Используемый файл с начальными данными: {initial_data_file}")

    # Даем пользователю время для корректировки начальных данных
    print("\nФайл с начальными данными создан/обновлен.")
    print(f"Пожалуйста, проверьте и при необходимости отредактируйте данные в файле {initial_data_file}.")
    input("После завершения редактирования нажмите Enter для продолжения...")

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
        print(f"Отчет успешно сгенерирован и сохранен в {report_path}")
    else:
        print("Ошибка при сохранении отчета")
