#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from design_of_mechanical_production.domain.entities.workshop import Workshop


class ReportGenerator(ABC):
    """
    Абстрактный класс для генерации отчетов.
    """
    
    @abstractmethod
    def generate_report(self, workshop: Workshop) -> str:
        """
        Генерирует отчет о цехе.
        
        Args:
            workshop: Объект цеха
            
        Returns:
            str: Текст отчета
        """
        pass
    
    @abstractmethod
    def save_report(self, report: str, filepath: str) -> bool:
        """
        Сохраняет отчет в файл.
        
        Args:
            report: Текст отчета
            filepath: Путь к файлу
            
        Returns:
            bool: Успешность сохранения
        """
        pass
