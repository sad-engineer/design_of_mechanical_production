#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль для работы с настройками.

Предоставляет функционал для:
- получения и установки настроек
- сохранения и загрузки настроек
"""
from design_of_mechanical_production.settings.manager import (
    DEFAULT_CONFIG,
    get_setting,
    set_setting,
)

__all__ = [
    # Функции
    'get_setting',
    'set_setting',
    'DEFAULT_CONFIG',
]
