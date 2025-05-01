#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import pandas as pd

from design_of_mechanical_production.settings import DEFAULT_CONFIG


def create_initial_data():
    # Данные о цехе
    parameters_data = {'name': ['Механический цех №1'], 'production_volume': [10000], 'mass_detail': [112.8]}  # Годовой объем производства в штуках

    # Данные о нормировании
    process_data = {
        'number': ["005", "010", "015", "020"],
        'name': ["Токарная с ЧПУ", "Расточная с ЧПУ", "Токарная с ЧПУ", "Фрезерная с ЧПУ"],
        'time': [11.6712, 20.8216, 5.6484, 1.8592],
        'machine': ["DMG CTX beta 2000", "2431СФ10", "DMG CTX beta 2000", "DMU 50"],
    }

    # Создаем DataFrame'ы
    df_parameters = pd.DataFrame(parameters_data)
    df_process = pd.DataFrame(process_data)

    # Создаем Excel файл
    with pd.ExcelWriter(DEFAULT_CONFIG['input_data_path'], engine='openpyxl') as writer:
        df_parameters.to_excel(writer, sheet_name='Parameters', index=False)
        df_process.to_excel(writer, sheet_name='Process', index=False)


if __name__ == "__main__":
    create_initial_data()
