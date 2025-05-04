#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Protocol


class IReportGenerator(Protocol):
    """
    Интерфейс для генерации отчетов.
    """

    def generate_report(self, workshop: 'IWorkshop') -> str:
        """
        Генерирует отчет о цехе.

        Args:
            workshop: Объект цеха

        Returns:
            str: Текст отчета
        """
        ...

    def save_report(self, report: str, filepath: str) -> bool:
        """
        Сохраняет отчет в файл.

        Args:
            report: Текст отчета
            filepath: Путь к файлу

        Returns:
            bool: Успешность сохранения
        """
        ...
