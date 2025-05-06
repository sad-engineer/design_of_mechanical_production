#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
from pathlib import Path

from design_of_mechanical_production.data.input import create_initial_data
from design_of_mechanical_production.settings import get_setting

INPUT_DATA_PATH = Path(get_setting('input_data_path'))
REPORT_PATH = Path(get_setting('report_path'))


def ensure_directories_exist() -> None:
    """
    Создает необходимые директории для входных и выходных данных, если они не существуют.

    Создает следующие директории:
    - Директория для входных данных (из настроек input_data_path)
    - Директория для выходных данных (из настроек report_path)
    """
    # Создаем директории для входных и выходных данных
    input_dir = INPUT_DATA_PATH.parent
    output_dir = REPORT_PATH.parent

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)


def check_initial_data_file() -> bool:
    """
    Проверяет существование файла с начальными данными.

    Returns:
        - bool: True если файл существует, False если нет
    """
    return os.path.exists(INPUT_DATA_PATH)


def create_initial_data_file() -> Path:
    """
    Создает файл с начальными данными, если он не существует.

    Выполняет следующие действия:
    1. Проверяет существование файла
    2. Если файл не существует, создает его
    3. Выводит сообщение о результате операции
    """
    file_exists = check_initial_data_file()
    if not file_exists:
        print("Файл с начальными данными не найден. Создаем новый файл...")
        create_initial_data()
        print("Файл с начальными данными успешно создан.")
    else:
        print(f"Файл с начальными данными уже существует: {INPUT_DATA_PATH}")
    return INPUT_DATA_PATH
