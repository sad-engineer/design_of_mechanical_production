#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Protocol
from design_of_mechanical_production.entities.workshop import Workshop


class IReportGenerator(Protocol):
    """
    Интерфейс для генерации отчетов.
    """
    def generate_report(self, workshop: Workshop) -> str:
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
