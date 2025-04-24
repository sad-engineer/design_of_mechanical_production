#------------------------------------------------------------------------------
# Name:        initial_data                                                          
# Purpose:     Модуль ввода начальных значений
#              
# Author:      ANKorenuk                                                        
#                                                                               
# Created:     07.11.2021                                                       
# Copyright:   (c) ANKorenuk 2021                                               
# Licence:     <your licence>                                                   
#------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
import pandas as pd    # для формирования таблиц данных  
from decimal import Decimal, ROUND_HALF_UP  # для округления
#------------------------------------------------------------------------------
#Блок констант
#TODO: внести в список настроек 

# Трудоемкость изготовления 1 тонны изделия. По умолчанию - 40 нормо-часа.
COMPLEXITY_NORM = 40.0  
   
#точность округления  
ORDER = 3 
            
#------------------------------------------------------------------------------
def round_off_result(variable, order=ORDER):
    """
    Функция округления.
    round - работает не так как надо
    round применяю только для выбора значений из таблиц, для отсечения 
    миллионных погрешностей

    Parameters
    ----------
    variable : float
        переменная или результат вычислений.
    order : int, optional
        точность округления. The default is ORDER.

    Returns
    -------
    variable : float
        Возвращает значение variable, округленное до order-знака после запятой.
        Округляет вверх, если цифра пять и больше.

    """
    
    if order > 0: 
        order = '1.' + '0'*order
    else: 
        order = '1'
        
    variable = Decimal(variable)
    variable = variable.quantize(Decimal(order), ROUND_HALF_UP)
    variable = float(variable)
    
    return variable


#------------------------------------------------------------------------------
def get_rationing_data():
    # Получение данных норирования техпроцесса
    # Должен получать данные после норирования техпроцесса в формате датафрейма
    #Должен содержать столбцы "№ операции", "Наименование операции", 
    # "Штучно-калькуляционное время"
   
    dict_initial_data = {}
    
    annual_output_volume = 10000
    mass_detail = 112.8 
    table_rationing_data = pd.DataFrame({ 
        'namber' : [              "005",             "010",               "015",             "020", ],
        'name'   : [   "Токарная с ЧПУ", "Расточная с ЧПУ",    "Токарная с ЧПУ", "Фрезерная с ЧПУ", ],
        'time'   : [              42.69,             76.16,               20.66,               6.8, ],
        'machine': ["DMG CTX beta 2000",    "УЦИ 2431СФ10", "DMG CTX beta 2000",  "DMG DMU 80 eVo", ],
    })
    
    dict_initial_data["annual_output_volume"] = annual_output_volume
    dict_initial_data["mass_detail"] = mass_detail
    dict_initial_data["table_rationing_data"] = table_rationing_data
    
    #!!! Организовать более  логичный ввод
    
    return dict_initial_data


def complexity_of_order_fulfillment(table_rationing_data, number, mass):
    # Определяет трудоемкость выполнения произвдственной программы
    table = table_rationing_data
    
    table = get_share_of_total_complexity(table)
    table = get_complexity_of_operations(table, number)
    
    return table
    

def get_share_of_total_complexity(table):
    # определяет долю операции от общей трудоемкости (в процентах)
    counts = table['time']
    percent = counts / counts.sum()
    fmt = '{:.3%}'.format
    percent = percent.map(fmt)
    table['per'] = percent
    
    return table


def get_complexity_of_operation(annual_output, 
                                percentage_of_operation,
                                complexity_norm=COMPLEXITY_NORM):   
    """
    Определяет трудоемкость i-той операции

    Parameters
    ----------
    annual_output : float
        годовой объём выпуска.
    percentage_of_operation : float
        Процентное содержание операции в общей трудоемкости изготовления детали.
    complexity_norm : float
        Трудоемкость изготовления 1 тонны изделия.

    Returns
    -------
    None.

    """
    complexity_of_operation = annual_output * percentage_of_operation * complexity_norm
    complexity_of_operation = round_off_result(complexity_of_operation)
    
    return complexity_of_operation


def get_complexity_of_operations(table, number):
    # Определяет трудоемкость каждой операциив таблице "table"
    
    per_values = table['per']
    dict_per_values = per_values.to_dict()
    dict_comp_op = {}
    
    for key, value in dict_per_values.items():
        value = float(value.replace("%",""))
        value = value / 100
        dict_comp_op[key] = get_complexity_of_operation(number, value)
    
    complexity_of_operations = pd.Series(dict_comp_op)
    table['comp_op'] = complexity_of_operations
    
    return table


def get_gabarit(table):
    # Определяет габариты станков
    # !!! сделать определение из базы данных
    gabarit = ["6234x2142x2052" , "2360x1900x1580", "6234x2142x2052", "2440x3350x3050"]
    table["gabarit"] = gabarit
    
    return table
    

#------------------------------------------------------------------------------
def main():
    # Ввод начальных данных
    # 1) годовой объем выпуска продукции в штуках
    # 2) Датафрейм техпроцесса (с наименованиями и последовательностью операций 
    # и штучным временем для каждой)
    
    
    rationing_data = get_rationing_data()
    
    table_rationing = complexity_of_order_fulfillment(
        rationing_data["table_rationing_data"],
        rationing_data["annual_output_volume"],
        rationing_data["mass_detail"],
        )
    
    table_rationing = get_gabarit(table_rationing)
    
    input_result = {}
    input_result["table_rationing"] = table_rationing
    input_result["annual_output_volume"] = rationing_data["annual_output_volume"]
    input_result["mass_detail"] = rationing_data["mass_detail"]
    input_result["complexity_norm"] = COMPLEXITY_NORM
    
    return input_result


#------------------------------------------------------------------------------
if __name__ == "__main__":
    result = main()
    # print (result["table_rationing"])
    # print (result["annual_output_volume"])
    # print (result["mass_detail"])
    # print (result["complexity_norm"])