#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
import yaml
import os
from pathlib import Path
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class ConfigRepository(ABC):
    """Абстрактный класс для работы с конфигурацией"""

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Загружает конфигурацию"""
        pass

    @abstractmethod
    def save(self, config: Dict[str, Any]) -> None:
        """Сохраняет конфигурацию"""
        pass


class YamlConfigRepository(ConfigRepository):
    """Реализация репозитория конфигурации для YAML файлов"""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            return {}

    def save(self, config: Dict[str, Any]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)


class ConfigManager:
    """Менеджер конфигурации"""

    def __init__(self, repository: ConfigRepository, default_config: Dict[str, Any]):
        self.repository = repository
        self.default_config = default_config
        self._config: Optional[Dict[str, Any]] = None

    @property
    def config(self) -> Dict[str, Any]:
        """Получает текущую конфигурацию"""
        if self._config is None:
            self._config = self.repository.load()
            if not self._config:
                self._config = self.default_config
                self.repository.save(self._config)
        return self._config

    def get_setting(self, key_path: str) -> Any:
        """
        Получает значение настройки по ключу (вложенные ключи через точку).
        
        Parameters
        ----------
        key_path : str
            Путь к настройке через точку (например, "common.paths.for_reports")
            
        Returns
        -------
        Any
            Значение настройки
            
        Raises
        ------
        ValueError
            Если настройка не найдена
        """
        try:
            value = self.config
            for key in key_path.split("."):
                value = value[key]
            return value
        except (KeyError, TypeError):
            raise ValueError(f"Ошибка: настройка '{key_path}' не найдена.")

    def set_setting(self, key_path: str, new_value: Any) -> None:
        """
        Изменяет значение настройки и сохраняет его.
        
        Parameters
        ----------
        key_path : str
            Путь к настройке через точку
        new_value : Any
            Новое значение настройки
        """
        try:
            config = self.config
            keys = key_path.split(".")
            temp = config
            for key in keys[:-1]:
                temp = temp.setdefault(key, {})
            temp[keys[-1]] = new_value

            self.repository.save(config)
            self._config = config  # Обновляем кэш
            print(f"Настройка '{key_path}' изменена на {new_value}.")
        except Exception as e:
            print(f"Ошибка при изменении настройки: {e}")


# Инициализация путей
cur_dir = Path(__file__).parent.parent
CONFIG_FILE = cur_dir / "settings.yaml"

# Настройки по умолчанию
DEFAULT_CONFIG = {
    # Действительный фонд времени работы одного станка, ч
    'fund_of_working': 4080,  
    # Коэффициенты
    'kv': 1.00,  # Коэффициент выполнения норм
    'kp': 1.45,  # Коэффициент прогрессивности технологии
    
    # Процентные соотношения для вспомогательных зон
    'grinding_zone_percent': 0.05,  # 5% для заточного отделения
    'repair_zone_percent': 0.025,  # 2.5% для ремонтного отделения
    
    # Настройки для расчета площади
    'passage_area': 10,  # Площадь для проходов между станками, м²
    
    # Удельные площади вспомогательных зон (м² на единицу)
    'specific_areas': {
        'tool_storage': 0.3,  # Склад инструмента
        'equipment_warehouse': 0.2,  # Склад приспособлений
        'work_piece_storage': 0.3,  # Склад заготовок
        'control_department': 0.05,  # Отделение контроля
        'sanitary_zone': 8,  # Санитарная зона
    }
}

# Создаем экземпляр менеджера конфигурации
config_repository = YamlConfigRepository(str(CONFIG_FILE))
config_manager = ConfigManager(config_repository, DEFAULT_CONFIG)


# Функции для удобства использования
def get_setting(key_path: str) -> Any:
    """Получает значение настройки по ключу (вложенные ключи через точку)."""
    return config_manager.get_setting(key_path)


def set_setting(key_path: str, new_value: Any) -> None:
    """Изменяет значение настройки и сохраняет его в config.yaml."""
    config_manager.set_setting(key_path, new_value)


# Автоматическое создание файла конфигурации при первом запуске
if not os.path.exists(CONFIG_FILE):
    config_manager.repository.save(DEFAULT_CONFIG)
    print(f"Файл {CONFIG_FILE} создан с начальными настройками.")
