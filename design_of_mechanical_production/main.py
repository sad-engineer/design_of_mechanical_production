#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from design_of_mechanical_production.data.utils.file_system import (
    check_initial_data_file,
    create_initial_data_file,
    ensure_directories_exist,
)
from design_of_mechanical_production.launch_manager import load_launch_config
from design_of_mechanical_production.launcher import run_with_gui, run_without_gui


def main():
    """
    Точка входа в приложение.

    Определяет режим запуска и запускает приложение
    в соответствующем режиме (с GUI или без).
    """
    # Проверяем наличие необходимых директорий
    ensure_directories_exist()
    # Проверяем наличие файла с начальными данными
    if not check_initial_data_file():
        create_initial_data_file()

    # Загружаем конфигурацию
    config = load_launch_config()

    # Запускаем в соответствующем режиме
    if config['mode'] == 'gui':
        print("Запуск в режиме GUI...")
        run_with_gui(theme=config["theme"])
    elif config['mode'] == 'console':
        print("Запуск в консольном режиме...")
        run_without_gui()
    else:
        print("Неверный режим запуска. Используйте 'gui' или 'console'.")


if __name__ == "__main__":
    main()
