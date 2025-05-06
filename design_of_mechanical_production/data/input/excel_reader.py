#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from design_of_mechanical_production.core.interfaces import IDataReader


class ExcelReader(IDataReader):
    """
    Класс для чтения данных из Excel файлов.
    """

    def __init__(self, filepath: Path):
        self.filepath = filepath

    def read_parameters_data(self) -> Dict[str, Any]:
        """
        Читает данные о цехе и параметрах из Excel.
        """
        try:
            df = pd.read_excel(self.filepath, sheet_name='Parameters')
            return {'name': df['name'].iloc[0], 'production_volume': int(df['production_volume'].iloc[0]), 'mass_detail': float(df['mass_detail'].iloc[0])}
        except Exception as e:
            raise Exception(f"Ошибка при чтении данных о параметрах: {str(e)}")

    def read_process_data(self) -> Dict[str, Any]:
        """
        Читает данные о технологическом процессе из Excel.
        """
        try:
            # Указываем тип данных для колонки number как строковый
            df = pd.read_excel(self.filepath, sheet_name='Process', dtype={'number': str})
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Ошибка при чтении данных о технологическом процессе: {str(e)}")
