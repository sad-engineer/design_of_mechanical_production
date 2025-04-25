#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from abc import ABC, abstractmethod
from typing import Dict, Any


class DataReader(ABC):
    """
    Абстрактный класс для чтения входных данных.
    """
    
    @abstractmethod
    def read_parameters_data(self) -> Dict[str, Any]:
        """
        Читает данные о цехе и параметрах.
        """
        pass
    
    @abstractmethod
    def read_equipment_data(self) -> Dict[str, Any]:
        """
        Читает данные об оборудовании.
        """
        pass
    
    @abstractmethod
    def read_worker_data(self) -> Dict[str, Any]:
        """
        Читает данные о рабочих.
        """
        pass
    
    @abstractmethod
    def read_process_data(self) -> Dict[str, Any]:
        """
        Читает данные о технологическом процессе.
        """
        pass
