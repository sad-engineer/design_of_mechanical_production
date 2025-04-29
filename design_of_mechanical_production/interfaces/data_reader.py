#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Dict, Any, Protocol


class IDataReader(Protocol):
    """
    Интерфейс для чтения входных данных.
    """
    def read_parameters_data(self) -> Dict[str, Any]:
        """
        Читает данные о цехе и параметрах.
        """
        ...
    
    def read_process_data(self) -> Dict[str, Any]:
        """
        Читает данные о технологическом процессе.
        """
        ...
