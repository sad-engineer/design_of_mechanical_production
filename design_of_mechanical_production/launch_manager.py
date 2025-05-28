#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Скрипт для управления режимом запуска приложения.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict


def load_launch_config() -> Dict[str, Any]:
    """
    Загружает конфигурацию запуска из файла.

    Returns:
        Dict[str, Any]: Конфигурация запуска приложения
    """
    config_path = Path(__file__).parent.parent / "settings" / 'design_launch_config.json'
    if not config_path.exists():
        # Создаем файл с настройками по умолчанию
        default_config = {'mode': 'gui', 'theme': 'Light'}  # 'Light' или 'Dark'
        save_launch_config(default_config)
        return default_config

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_launch_config(config: Dict[str, Any]) -> None:
    """
    Сохраняет конфигурацию запуска в файл.

    Args:
        config: Конфигурация запуска приложения
    """
    config_path = Path(__file__).parent.parent / "settings" / 'design_launch_config.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def set_launch_mode(mode: str) -> None:
    """
    Устанавливает режим запуска приложения.

    Args:
        mode: Режим запуска ('gui' или 'console')
    """
    if mode not in ['gui', 'console']:
        print("Неверный режим. Используйте 'gui' или 'console'.")
        sys.exit(1)

    config = load_launch_config()
    config['mode'] = mode
    save_launch_config(config)
    print(f"Режим запуска успешно изменен на '{mode}'.")


def set_theme(theme: str) -> None:
    """
    Устанавливает тему приложения.

    Args:
        theme: Тема приложения ('light' или 'dark')
    """
    # Преобразуем ввод в правильный формат
    theme = theme.capitalize()

    if theme not in ['Light', 'Dark']:
        print("Неверная тема. Используйте 'light' или 'dark'.")
        sys.exit(1)

    config = load_launch_config()
    config['theme'] = theme
    save_launch_config(config)
    print(f"Тема успешно изменена на '{theme}'.")


def show_launch_config() -> None:
    """
    Показывает текущие настройки запуска.
    """
    config = load_launch_config()
    print("\nТекущие настройки запуска:")
    for key, value in config.items():
        print(f"  {key}: {value}")


def main():
    """
    Точка входа в скрипт управления режимом запуска.
    """
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python -m design_of_mechanical_production.launch_manager show  - показать текущие настройки запуска")
        print("  python -m design_of_mechanical_production.launch_manager gui   - установить режим GUI")
        print("  python -m design_of_mechanical_production.launch_manager console - установить консольный режим")
        print("  python -m design_of_mechanical_production.launch_manager theme light - установить светлую тему")
        print("  python -m design_of_mechanical_production.launch_manager theme dark  - установить темную тему")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'show':
        show_launch_config()
    elif command in ['gui', 'console']:
        set_launch_mode(command)
    elif command == 'theme':
        if len(sys.argv) < 3:
            print("Укажите тему: light или dark")
            sys.exit(1)
        set_theme(sys.argv[2].lower())
    else:
        print("Неизвестная команда. Используйте 'show', 'gui', 'console' или 'theme'.")
        sys.exit(1)
