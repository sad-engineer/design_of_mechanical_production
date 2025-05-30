#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import pandas as pd

from design_of_mechanical_production.settings import get_setting

INPUT_DATA_PATH = str(get_setting('input_data_path'))


def create_initial_data():
    # Данные о цехе
    parameters_data = {'name': ['Механический цех №1'], 'production_volume': [10000], 'mass_detail': [112.8]}

    # Данные о нормировании
    process_data = {
        'number': ["005", "010", "015", "020"],
        'name': ["Токарная с ЧПУ", "Расточная с ЧПУ", "Токарная с ЧПУ", "Фрезерная с ЧПУ"],
        'time': [11.6712, 20.8216, 5.6484, 1.8592],
        'machine': ["1325Ф30", "24К40СФ4", "1325Ф30", "6720ВФ2Ф2"],
    }

    # Создаем DataFrame'ы
    df_parameters = pd.DataFrame(parameters_data)
    df_process = pd.DataFrame(process_data)

    # Создаем Excel файл
    with pd.ExcelWriter(INPUT_DATA_PATH, engine='openpyxl') as writer:
        df_parameters.to_excel(writer, sheet_name='Parameters', index=False)
        df_process.to_excel(writer, sheet_name='Process', index=False)


if __name__ == "__main__":
    create_initial_data()
