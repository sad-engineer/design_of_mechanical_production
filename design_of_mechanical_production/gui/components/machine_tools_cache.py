#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит константы и утилиты для работы со станками.
"""
import os
import json
import pickle
from typing import List, Any, Optional, Dict
import pkg_resources
from machine_tools import MachineToolsContainer as Container


class MachineToolsCache:
    """
    Кэш для списка станков с проверкой версии.
    """
    CACHE_DIR = os.path.join(os.path.dirname(__file__), '.cache')
    CACHE_FILE = os.path.join(CACHE_DIR, 'machine_tools.pkl')
    VERSION_FILE = os.path.join(CACHE_DIR, 'version.json')

    def __init__(self):
        """Инициализирует кэш и проверяет версию."""
        self._ensure_cache_dir()
        self._tools_names: Optional[List[Any]] = None
        self._current_version = self._get_current_version()
        self._load_cache()

    def _ensure_cache_dir(self):
        """Создает директорию для кэша, если она не существует."""
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

    @staticmethod
    def _get_current_version() -> str:
        """
        Получает текущую версию machine_tools.

        Returns:
            str: Текущая версия.
        """
        try:
            return pkg_resources.get_distribution('machine_tools').version
        except pkg_resources.DistributionNotFound:
            # Если пакет не установлен через pip, используем хеш данных
            lister = Container().lister()
            tools = lister.all
            tools_names = [tool.name for tool in tools]
            return str(hash(str(tools_names)))

    def _load_cache(self):
        """Загружает данные из кэша или создает новые."""
        if not os.path.exists(self.CACHE_FILE) or not os.path.exists(self.VERSION_FILE):
            self._update_cache()
            return

        try:
            with open(self.VERSION_FILE, 'r', encoding='utf-8') as f:
                cached_version = json.load(f).get('version')

            if cached_version != self._current_version:
                self._update_cache()
                return

            with open(self.CACHE_FILE, 'rb') as f:
                self._tools_names = pickle.load(f)
        except (json.JSONDecodeError, pickle.UnpicklingError, FileNotFoundError):
            self._update_cache()

    def _update_cache(self):
        """Обновляет кэш новыми данными."""
        lister = Container().lister()
        self._tools_names = [tool.name for tool in lister.all]

        # Сохраняем версию
        with open(self.VERSION_FILE, 'w', encoding='utf-8') as f:
            json.dump({'version': self._current_version}, f)

        # Сохраняем данные
        with open(self.CACHE_FILE, 'wb') as f:
            pickle.dump(self._tools_names, f)

    @property
    def tools(self) -> List[Any]:
        """
        Возвращает кэшированный список станков.

        Returns:
            List[Any]: Список доступных станков.
        """
        return self._tools_names


# Создаем экземпляр кэша
_cache = MachineToolsCache()

# Список всех доступных станков
MACHINE_TOOLS = _cache.tools


def get_machine_tools() -> List[Any]:
    """
    Возвращает кэшированный список станков.

    Returns:
        List[Any]: Список доступных станков.
    """
    return MACHINE_TOOLS
