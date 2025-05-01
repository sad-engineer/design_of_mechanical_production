#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from design_of_mechanical_production.core.launcher import run_with_gui, run_without_gui
from design_of_mechanical_production.launch_manager import load_launch_config


def main():
    """
    Точка входа в приложение.

    Определяет режим запуска и запускает приложение
    в соответствующем режиме (с GUI или без).
    """
    # Загружаем конфигурацию
    config = load_launch_config()

    # Запускаем в соответствующем режиме
    if config['mode'] == 'gui':
        print("Запуск в режиме GUI...")
        run_with_gui()
    elif config['mode'] == 'console':
        print("Запуск в консольном режиме...")
        run_without_gui()
    else:
        print("Неверный режим запуска. Используйте 'gui' или 'console'.")


if __name__ == "__main__":
    main()
