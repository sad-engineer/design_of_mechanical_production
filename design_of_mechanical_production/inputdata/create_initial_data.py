#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from decimal import Decimal


def create_initial_data():
    # Данные о цехе
    parameters_data = {
        'name': ['Механический цех №1'],
        'production_volume': [10000],  # Годовой объем производства в штуках
        'mass_detail': [112.8]
    }
    
    # Данные о рабочих
    workers_data = {
        'name': [
            'Иванов И.И.',
            'Петров П.П.',
            'Сидоров С.С.',
            'Козлов К.К.'
        ],
        'position': [
            'Токарь',
            'Фрезеровщик',
            'Сверловщик',
            'Шлифовщик'
        ],
        'qualification': [4, 5, 3, 4],
        'hourly_rate': [
            Decimal('250'),
            Decimal('300'),
            Decimal('200'),
            Decimal('250')
        ]
    }
    
    # Данные о нормировании
    process_data = {
        'number': ["005", "010", "015", "020"],
        'name': [
            "Токарная с ЧПУ",
            "Расточная с ЧПУ",
            "Токарная с ЧПУ",
            "Фрезерная с ЧПУ"
        ],
        'time': [11.6712, 20.8216, 5.6484, 1.8592],
        'machine': [
            "DMG CTX beta 2000",
            "2431СФ10",
            "DMG CTX beta 2000",
            "DMU 50"
        ]
    }
    
    # Создаем DataFrame'ы
    df_parameters = pd.DataFrame(parameters_data)
    df_equipment = pd.DataFrame(equipment_data)
    df_workers = pd.DataFrame(workers_data)
    df_process = pd.DataFrame(process_data)
    
    # Создаем Excel файл
    with pd.ExcelWriter('inputdata/initial_data.xlsx', engine='openpyxl') as writer:
        df_parameters.to_excel(writer, sheet_name='Parameters', index=False)
        df_equipment.to_excel(writer, sheet_name='Equipment', index=False)
        df_workers.to_excel(writer, sheet_name='Workers', index=False)
        df_process.to_excel(writer, sheet_name='Process', index=False)


if __name__ == "__main__":
    create_initial_data()
