#------------------------------------------------------------------------------
# Name:        calculation                                                          
# Purpose:     Модуль расчета конечных значений
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
from decimal import Decimal, ROUND_HALF_UP  # для округления
import pandas as pd    # для формирования таблиц данных  
import numpy as np
from math import ceil
#------------------------------------------------------------------------------
#Блок констант
#TODO: внести в список настроек 

# действительный фонд времени работы одного станка, ч
FUND_OF_WORKING = 4080
# действительный годовой фонд времени рабочего, ч
FUND_OF_WORKER = 1850

# коэффициент выполнения норм, принимается ориентировочно 1,1... 1,25
KV = 1.15
# коэффициент прогрессивности технологии проектируемого цеха
KP = 1.45

# Коэффициент для расчета заточных станков
K_C_ZAT = 0.05

# Коэффициент для расчета ремонтных станков
K_C_REM = 0.025

#точность округления  
ORDER = 3 

# профиль состава производственных рабочих
# Процентное распределение рабочих по разрядам
PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS = {
    "profile_1": [ 0,  0, 20, 40, 40, 0],
    "profile_2": [ 0,  0, 15, 40, 40, 5],
    "profile_3": [ 5, 10, 20, 30, 30, 5],
    }
# фдаг выбранного профиля
SELECTED_PROFILE = "profile_1"

# отношение вспомогательных рабочих к производственным
KPVSP = 0.25

PROFESSIONS = {
    "Токарная": "Токарь",
    "Токарная с ЧПУ": "Токарь",
    "Расточная": "Токарь",
    "Расточная с ЧПУ": "Токарь",
    "Фрезерная": "Фрезеровщик",
    "Фрезерная с ЧПУ": "Фрезеровщик",
    "Сверлильная": "Сверлильщик",
    "Сверлильная с ЧПУ": "Сверлильщик",
    "Шлифовальная": "Шлифовальщик",
    "Шлифовальная с ЧПУ": "Шлифовальщик",
    None: None,
    }   

# удельная площадь склада инструмента на 1 станок, в зависимостиот вида 
# производства при работе в 2 смены
S_UD_SI = 0.3

# удельная площадь склада приспособлений на 1 станок;
S_UD_SP = 0.2

# Коэффициент для расчета площади промежуточных складов (30%)
K_S_SKP = 0.3

# Коэффициент для расчета площади контрольного отделения (5%)
K_S_KONTR = 0.05

# количество санузлов
N_SAN = 2
# площадь одного санузла, м^2
S_UD_SAN = 8

# ширина пролета цеха 
WORKSHOP_SPAN = 12
WORKSHOP_NAM = 3
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
def determine_kv(data):
    # Определяет коэффициент выполнения норм
    # коэффициент выполнения норм, принимается ориентировочно 1,1... 1,25; 
    # для станков с ЧПУ его следует принимать равным 1
    # !!! переделать на запрос к БД
    list_kv = []
    names = data["name"].to_list()
    for name in names:
        if name.find("с ЧПУ") != -1:
            kv = 1.0
        else:
            kv = KV
        list_kv.append(kv)
    data["kv"] = list_kv
    
    return(data)


def determine_km(data):
    # Определяет коэффициент коэффициент многостаночности
    # коэффициент выполнения норм, принимается 1 - для универсальных токарных, 
    # сверлильных, фрезерных, круглошлифовальных, станков непрерывного действия 
    # и др.; 1,5 - – для токарных многорезцовых станков, токарных полуавтоматов.
    # !!! переделать на запрос к БД
    list_km = []
    names = data["name"].to_list()
    for name in names:
        if name.find("с ЧПУ") != -1:
            km = 1.5
        else:
            km = 1
        list_km.append(km)
    data["km"] = list_km
    
    return(data)


def number_of_machines_per_operation(complexity_norm,
                                     kv,
                                     fund_of_working=FUND_OF_WORKING,
                                     kp=KP,):
    # Расчётное количество станков 
    num_mach = complexity_norm/(fund_of_working * kv * kp)
    num_mach = round_off_result(num_mach)
    
    return num_mach


def number_of_machines(data,
                       fund_of_working=FUND_OF_WORKING,
                       kp=KP):
    # Расчёт необходимого количества оборудования по датафрейму "data"
    n_of_m = []
    
    for index, row in data.iterrows():
        comp_op = row["comp_op"]
        kv = row["kv"]
        number_of_machines = number_of_machines_per_operation(
            comp_op,
            kv,
            fund_of_working,
            kp)
        n_of_m.append(number_of_machines)
    
    data["num_of_mach"] = n_of_m
    
    return data


def distribute_by_estates(table,
                          column="accepted_num_operators",
                          name_suf="",
                          selected_profile=SELECTED_PROFILE,
                          ):
    
    # Делает распределение количества по шаблону. Например, распределение 
    # операторов станков и вспомогательных рабочих по разрядам работы
    digit_names = []
    
    if name_suf != "" or not isinstance(name_suf, type(None)):
        name_suf = str(name_suf) + "_"
        
    if isinstance(selected_profile, list):
        for i in range(len(selected_profile)):
            name = "digit_" + str(name_suf) + str(i+1)
            digit_names.append(name)
            table[name] = table[column]
            table[name] *= selected_profile[i]
            table[name] = table[name].map(round)
    elif selected_profile in PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS:
        for i in range(len(PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS[selected_profile])):
            name = "digit_" + str(name_suf) + str(i+1)
            digit_names.append(name)
            table[name] = table[column]
            table[name] *= (PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS[selected_profile][i]/100)
            table[name] = table[name].map(round)
    servis_table = table[digit_names]
    
    list_num = []
    digits = PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS[selected_profile].copy() 
    for digit in digits:
        if digit != 0:
            list_num.append(digit)
            
    min_num = min(list_num) 
    name_min_num = "digit_" + str(name_suf) + str(
        PROFILES_OF_COMPOSITION_OF_PRODUCTION_WORKERS[selected_profile].index(
            min_num) + 1)
    
    for index, row in servis_table.iterrows():
        if sum(row) != table[column][index]:
            difference = sum(row) - table[column][index]
            correct_val = table[name_min_num][index] - difference
            table.loc[index, name_min_num] = correct_val
            
    return table


def main(data, 
         fund_of_working=FUND_OF_WORKING,
         fund_of_worker=FUND_OF_WORKER,
         kp=KP,
         selected_profile=SELECTED_PROFILE,
         KPvsp=KPVSP,
         K_c_zat=K_C_ZAT,
         K_c_rem=K_C_REM,
         S_ud_si=S_UD_SI,
         S_ud_sp=S_UD_SP,
         K_s_skp=K_S_SKP,
         K_s_kontr=K_S_KONTR,
         N_san=N_SAN,
         S_ud_san=S_UD_SAN,
         workshop_span=WORKSHOP_SPAN,
         workshop_nam=WORKSHOP_NAM,
         ):
    # Обработка данных: Расчет количества оборудования, загрузки, рабочих и площадей
    processing_result = {}
    
    table = data["table_rationing"]
    
    annual_output_volume = data["annual_output_volume"]
    processing_result["annual_output_volume"] = annual_output_volume
    
    mass_detail = data["mass_detail"]
    processing_result["mass_detail"] = mass_detail
    
    complexity_norm = data["complexity_norm"]
    processing_result["complexity_norm"] = complexity_norm
    
    # ========================================================================
    # Расчёт необходимого количества оборудования и его загрузки 
    table = determine_kv(table)
    
    processing_result["kp"] = kp
    table = number_of_machines(table, fund_of_working, kp)
    
    accepted_number_of_machines = list(table["num_of_mach"].map(ceil))
    table["accepted_num_of_mach"] = accepted_number_of_machines
    table = table.astype({'accepted_num_of_mach': np.int16})
    
    load_factor = list(map(lambda x, y: round_off_result(x/y), table["num_of_mach"], table["accepted_num_of_mach"]))
    table["load_factor"] = load_factor
    total_load_factor = round_off_result(sum(table["num_of_mach"])/sum(table["accepted_num_of_mach"]))
    # !!!
    C_zat = K_c_zat * sum(accepted_number_of_machines)
    accepted_C_zat = ceil(C_zat)
    processing_result["C_zat"] = C_zat
    processing_result["K_c_zat"] = K_c_zat
    processing_result["accepted_C_zat"] = accepted_C_zat
    
    C_rem = K_c_rem * sum(accepted_number_of_machines)
    accepted_C_rem = ceil(C_rem)
    processing_result["C_rem"] = C_rem
    processing_result["K_c_rem"] = K_c_rem
    processing_result["accepted_C_rem"] = accepted_C_rem
    
    C_ob = sum(accepted_number_of_machines) + accepted_C_rem + accepted_C_zat
    processing_result["C_ob"] = C_ob
    
    
    # ========================================================================
    # Расчет численности работающих
    table = determine_km(table)
    
    num_operators = list(map(lambda x, y, z: round_off_result( (x * y)/z), 
                             table["accepted_num_of_mach"], 
                             table["load_factor"],
                             table["km"],
                             ))
    processing_result["fund_of_working"] = fund_of_working
    processing_result["fund_of_worker"] = fund_of_worker
    num_operators = [round_off_result(i * fund_of_working / fund_of_worker) 
                     for i in num_operators]
    table["num_operators"] = num_operators
    
    accepted_num_operators = list(table["num_operators"].map(ceil))
    table["accepted_num_operators"] = accepted_num_operators
    table = table.astype({'accepted_num_operators': np.int16})
    
    table = distribute_by_estates(table,
                                  column="accepted_num_operators",
                                  name_suf="op",
                                  selected_profile=SELECTED_PROFILE,
                                  )
    
    names_op = table["name"]
    list_professions = []
    for name in names_op:
        if name in PROFESSIONS:
            list_professions.append(PROFESSIONS[name])
        else:
            list_professions.append("Профессия не установлена")
    
    table["professions"] = list_professions
    
    
    # Сводная ведомость состава вспомогательных рабочих цеха
    table_auxiliary_workers = pd.DataFrame()
    num_auxiliary_workers = int(ceil(sum(table["accepted_num_operators"]) * KPvsp))
    processing_result["num_auxiliary_workers"] = num_auxiliary_workers
    distribution = {"Наладчики": 0.25,
                    "Крановщики": 0.15,
                    "Контролеры": 0.20,
                    "Слесаря по ремонту оборудования": 0.35,
                    "Кладовщик": 0.05}
    for key, value in distribution.items():
        distribution[key] = int(round_off_result(value * num_auxiliary_workers, 0))
    if sum(distribution.values()) != num_auxiliary_workers:
        difference = num_auxiliary_workers - sum(distribution.values())
        distribution["Кладовщик"] = distribution["Кладовщик"] - difference
    
    for key, value in distribution.items():
        serw_row = {"professions": key,
                    "num_auxiliary_workers": value,
                    }
        table_auxiliary_workers = table_auxiliary_workers.append(serw_row, ignore_index=True)
    table_auxiliary_workers = distribute_by_estates(table_auxiliary_workers,
        column="num_auxiliary_workers",
        name_suf="aux",
        selected_profile=SELECTED_PROFILE,
        )
    table_auxiliary_workers = table_auxiliary_workers.transpose()
    table_auxiliary_workers["total"] = table_auxiliary_workers.sum(axis=1)
    table_auxiliary_workers = table_auxiliary_workers.transpose()
    table_auxiliary_workers.loc["total"]["professions"] = "Итого:"
    processing_result["table_auxiliary_workers"] = table_auxiliary_workers
    
    
    workers = sum(table["accepted_num_operators"]) + num_auxiliary_workers
    processing_result["workers"] = workers
    
    P_MOP = round_off_result((2.5 / 100) * workers)
    P_MOP_accept = ceil(P_MOP)
    processing_result["P_MOP"] = P_MOP
    processing_result["P_MOP_accept"] = P_MOP_accept
    
    P_SKP = round_off_result((15 / 100) * workers)
    P_SKP_accept = ceil(P_SKP)
    processing_result["P_SKP"] = P_SKP
    processing_result["P_SKP_accept"] = P_SKP_accept
    
    P_ITR = round_off_result((12 / 100) * workers)
    P_ITR_accept = ceil(P_ITR)
    processing_result["P_ITR"] = P_ITR
    processing_result["P_ITR_accept"] = P_ITR_accept
    
    people = pd.DataFrame()
    category_and_quantity = {
        "Основные рабочие": workers,
        "Вспомогательные рабочие": num_auxiliary_workers,
        "Инженернотехнические работники (ИТР)": P_ITR_accept,
        "Счетно-конторский персонал (СКП)": P_SKP_accept,
        "Младший обслуживающий персонал (МОП)": P_MOP_accept,
        }
    for key, value in category_and_quantity.items():
        row = {"category":key,
               "quantity":value,
               }
        people = people.append(row, ignore_index=True)
    people = people.transpose()
    people["total"] = people.sum(axis=1)
    people = people.transpose()
    people.loc["total"]["category"] = "Итого:"
    value_proc_op = float(people.loc[people["category"] == "Основные рабочие"]
                          ["quantity"])
    people["proc_op"] = (100 * people["quantity"] / value_proc_op).apply(
        lambda x: round(x, 3))
    value_proc_all = float(people.loc[people["category"] == "Итого:"]
                           ["quantity"])
    people["proc_all"] = (100 * people["quantity"] / value_proc_all).apply(
        lambda x: round(x, 3))
    people = people.astype({'quantity': np.int16})
    processing_result["people"] = people
    
    # ========================================================================
    # Расчёт площади участка
            
    L = list(map(lambda x: x.split("x")[0], table["gabarit"]))
    L = [round_off_result(int(i)/ 1000) for i in L]
    table["L"] = L
    
    B = list(map(lambda x: x.split("x")[1], table["gabarit"]))
    B = [round_off_result(int(i)/ 1000) for i in B]
    table["B"] = B
    
    S_CP = list(map(lambda x, y, z: (x*y + 10)*z, 
                    table["L"], 
                    table["B"], 
                    table["accepted_num_of_mach"],))
    S_CP = [round_off_result(i) for i in S_CP]
    table["S_CP"] = S_CP
    
    # ========================================================================
    # 4	Корректировка компоновки технологического оборудования дополнительными площадями
    
    S_si = round_off_result(S_ud_si * C_ob)
    processing_result["S_ud_si"] = S_ud_si
    processing_result["S_si"] = S_si
    
    S_sp = round_off_result(S_ud_sp * C_ob)
    processing_result["S_ud_sp"] = S_ud_sp
    processing_result["S_sp"] = S_sp
    
    S_irk = S_si + S_sp
    processing_result["S_irk"] = S_irk
    
    S_skp = round_off_result(K_s_skp * sum(S_CP))
    processing_result["K_s_skp"] = K_s_skp
    processing_result["S_skp"] = S_skp
    
    S_kontr = round_off_result(K_s_kontr * sum(S_CP))
    processing_result["K_s_kontr"] = K_s_kontr
    processing_result["S_kontr"] = S_kontr
    
    S_san = N_san * S_ud_san
    processing_result["N_san"] = N_san
    processing_result["S_ud_san"] = S_ud_san
    processing_result["S_san"] = S_san
    
    S_dop = round_off_result(S_kontr + S_san)
    processing_result["S_dop"] = S_dop
    
    S_workshop = round_off_result(sum(S_CP) + S_irk + S_skp + S_dop)
    processing_result["S_workshop"] = S_workshop
    
    # !!! сюда уточнение для workshop_span и workshop_nam
    L_workshop_span = round_off_result(S_workshop / (workshop_span * workshop_nam))
    processing_result["workshop_span"] = workshop_span
    processing_result["workshop_nam"] = workshop_nam
    processing_result["L_workshop_span"] = L_workshop_span
    
    
    # ========================================================================
    # Подсчет итоговых результатов  
    col = []
    for i in range(len(table.columns)):
        if table.columns[i].find("digit") != -1:
            col.append(table.columns[i])
    replace_table = table[["time", 
                           "comp_op",
                           "num_of_mach", 
                           "accepted_num_of_mach",
                           "num_operators",
                           "accepted_num_operators",
                           "S_CP",
                           # "digit_op_1",
                           # "workers",
                           ] + col]
    replace_table = replace_table.transpose()
    replace_table["total"] = replace_table.sum(axis=1)
    replace_table = replace_table.transpose()
    
    table = table.transpose()
    table["total"] = None
    table = table.transpose()
    for column in list(table.columns):
        if column in replace_table.columns:
            table[column] = replace_table[column]
            
    table.loc["total", "load_factor"] = total_load_factor
    
    # ========================================================================
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(table)
    
    
    
    processing_result["calculated_data"] = table
    
    return processing_result


if __name__ == "__main__":
    
    main()