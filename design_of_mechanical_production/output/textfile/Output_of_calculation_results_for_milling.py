#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#-------------------------------------------------------------------------------
# Name:        Output to file  * .docx calculation of miling modes
# Purpose:     Print the calculated data to a report
#
# Author:      ANKorenuk
#
# Created:     01.01.2020
# Copyright:   (c) ANKorenuk 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys

# u'читаю путь текущей дирректории'
cur_dir = os.path.abspath(os.curdir)

#Подключаем сценарий расчета
try:
    sys.path.append(cur_dir+'\\Out\\OutputWord')
    from OutputWord import OutputDataToDocx
except ImportError:
   sys.path.append(cur_dir+'\\OutputWord')
   from OutputWord import OutputDataToDocx
d = OutputDataToDocx()

# Для замены точки на запятую
try:
    from string import maketrans   # Python 2
except ImportError:
    maketrans = str.maketrans      # Python 3

#Подключаем модуль печати переменной и ее значения
from val_to_con import print_var

#------------------------------------------------------------------------------
# Убрать после соединения с основой
#from decimal import Decimal, ROUND_HALF_UP 


def dc(price):
    #Заменяет точку у значений float переменных на запятую при печати в строку.
    #Возвращает строку типа str
    price = price.translate(maketrans(',.', '.,'))
    return (price)


#------------------------------------------------------------------------------
def text(string, text_alignment=3):
    """
    Вывод текста. Исключительно для краткости записи
    """
    d.output_a_string_in_docx(string, text_alignment)
    
    
def form(string):
    """
    Вывод формулы. Исключительно для краткости записи
    """
    d.output_a_formula_in_docx(string)
    
    
def calc(formula, dimension, data):
    """
    Вывод формулы. Исключительно для краткости записи
    """
    d.output_of_calculations_in_docx(formula, dimension, data)
    
    
def var(string, name_variable, text_alignment=3):
    """
    Вывод формулы. Исключительно для краткости записи
    """
    d.output_text_with_the_variable_name(string, name_variable, text_alignment)


def output_of_calculation_results(mat, sigv, HB, dia, roughness, HRC, gr, mat_R, mat_r, z, type_of_treatment, type_of_milling_cutter, type_of_milling, flow_direction, type_of_cutting_part_of_the_milling_cutter, hard_MFTD, N_lathe_passport, B, pz, kind_of_cut, tabl_2_col_i, tabl_3_col_i, tabl_4_col_i, tabl_10_col_i, large_tooth, fi, Sz_tabl, Sz_take, Sz, So_tabl, So_take, So, KS, T, KMV, KG, nV, KPV, KIV, KV, CV, q_V, X_V, Y_V, u_V, p, m,  V_calc, KVfi, V, n_calculated, n_passport, n, V_actual, KMP, nP, CP, X_P, Y_P, u_P, q, w, Pz, K_tabl_Px, K_Px, Px, KfiP_Px, K_tabl_Py, K_Py, Py, KfiP_Py, K_tabl_Ph, K_Ph, Ph, K_tabl_Pv, K_Pv, Pv, Pxy, MKR, N, N_spindle, gr_cor, performance):
    
    print(u"Полученные для вывода данные:")
    print_var('mat, sigv, HB, dia, roughness, HRC, gr, mat_R, mat_r, z, type_of_treatment, type_of_milling_cutter, type_of_milling, flow_direction, type_of_cutting_part_of_the_milling_cutter, hard_MFTD, N_lathe_passport, B, pz, kind_of_cut, tabl_2_col_i, tabl_3_col_i, tabl_4_col_i, tabl_10_col_i, large_tooth, fi, Sz_tabl, Sz_take, Sz, So_tabl, So_take, So, KS, T, KMV, KG, nV, KPV, KIV, KV, CV, q_V, X_V, Y_V, u_V, p, m,  V_calc, KVfi, V, n_calculated, n_passport, n, V_actual, KMP, nP, CP, X_P, Y_P, u_P, q, w, Pz, K_tabl_Px, K_Px, Px, KfiP_Px, K_tabl_Py, K_Py, Py, KfiP_Py, K_tabl_Ph, K_Ph, Ph, K_tabl_Pv, K_Pv, Pv, Pxy, MKR, N, N_spindle, gr_cor, performance')
    
    #--------------------------------------------------------------------------
    text(u"Производим  расчет режимов резания для перехода 1.")
    #--------------------------------------------------------------------------
    text(u"Глубина резания:")
    text(u't = '+dc(str(gr))+u' мм.', 1)
    #--------------------------------------------------------------------------
    text(u"Определяю подачу: ")
    if type_of_treatment == 0 or type_of_treatment == 1: #черновая, получистовая
        if type_of_milling_cutter == 0 or type_of_milling_cutter == 1 or type_of_milling_cutter == 2 or type_of_milling_cutter == 3: 
            #"Цилиндрическая"
            #"Торцовая"
            #"Дисковая, обработка торца"
            #"Дисковая, обработка паза"
            if mat_R == 1:
                tabl = u"33"
                if mat == 5:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для алюминия и его сплавов табличное значение подачи не определено. Поэтому, берем как для меди: ")
                else:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
                form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/зуб.')
                if B > 30:
                    text(u"Принимаю: ")
                    form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                    text(u"C учетом примечаний табл. " + tabl + u", поскольку ширина резания более 30 мм, подачу рекомендуют умньшать на 30%. Поэтому итоговая зависимость для определения подачи будет иметь вид:")
                    form(u'S_Z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
                else:
                    text(u"Принимаю: ")
                    form(u'S_Z = '+dc(str(Sz_take))+u' мм/зуб.')
                    
            elif mat_R == 0:
                tabl = u"34"
                if mat == 5:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для алюминия и его сплавов табличное значение подачи не определено. Поэтому, берем как для меди: ")
                elif mat == 1:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для жаропрочной стали, с учетом требований примечания к данной таблице: ")
                elif mat == 2:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для закаленной стали, с учетом требований примечания к данной таблице: ")
                else:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
                form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/об.')
                text(u"Принимаю: ")
                form(u'S_Z = '+dc(str(Sz))+u' мм/зуб.')
        elif type_of_milling_cutter == 4 or type_of_milling_cutter == 7 or type_of_milling_cutter == 8 or type_of_milling_cutter == 9: 
            #"Отрезная"
            #"Угловая"
            #"Фасонная, с выпуклым профилем"
            #"Фасонная, с вогнутым профилем"
            tabl = u"35"
            if mat_R == 0:
                text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
                form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/зуб.')
            else:
                if type_of_milling_cutter == 4:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для отрезных фрез с пластинами из твердого сплава табличное значение подачи не определено. Поэтому, берем как для фрез с пластинами из быстрорежущей стали: ")
                elif type_of_milling_cutter == 7:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для угловых фрез с пластинами из твердого сплава табличное значение подачи не определено. Поэтому, берем как для фрез с пластинами из быстрорежущей стали: ")
                elif type_of_milling_cutter == 8 or type_of_milling_cutter == 9:
                    text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Для фасонных фрез с пластинами из твердого сплава табличное значение подачи не определено. Поэтому, берем как для фрез с пластинами из быстрорежущей стали: ")
                form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/зуб.')
                
            if mat == 3 or mat == 4:
                text(u"Принимаю: ")
                form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                text(u"При фрезеровании чугуна подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                form(u'S_z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
            elif mat == 5:
                text(u"Принимаю: ")
                form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                text(u"При фрезеровании медных сплавов подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                form(u'S_z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
            elif mat == 6:
                text(u"Принимаю: ")
                form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                text(u"При фрезеровании алюминиевых сплавов подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                form(u'S_z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
            else:
                text(u"Принимаю: ")
                form(u'S_z = '+dc(str(Sz))+u' мм/зуб.')
            
        elif type_of_milling_cutter == 5 or type_of_milling_cutter == 6: 
            #"Концевая, обработка торца"
            #"Концевая, обработка паза"
            if mat_R == 0:
                tabl = u"35"
            else:
                tabl = u"36"
            text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
            form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/зуб.')
            if mat_R == 0:
                if mat == 3 or mat == 4:
                    text(u"Принимаю: ")
                    form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                    text(u"При фрезеровании чугуна подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                    form(u'S_Z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
                elif mat == 5:
                    text(u"Принимаю: ")
                    form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                    text(u"При фрезеровании медных сплавов подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                    form(u'S_Z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
                elif mat == 6:
                    text(u"Принимаю: ")
                    form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                    text(u"При фрезеровании алюминиевых сплавов подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                    form(u'S_Z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
                else:
                    text(u"Принимаю: ")
                    form(u'S_z = '+dc(str(Sz))+u' мм/зуб.')
            else:
                if mat == 3 or mat == 4:
                    text(u"Принимаю: ")
                    form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
                    text(u"При фрезеровании чугуна подачи рекомендуют увеличивать 30-40%. Поэтому итоговая зависимость для определения подачи будет иметь вид: ")
                    form(u'S_Z = '+dc(str(KS))+u' * '+dc(str(Sz_take))+u' = '+dc(str(Sz))+u' мм/зуб.')
                else:
                    text(u"Принимаю: ")
                    form(u'S_Z = '+dc(str(Sz))+u' мм/зуб.')
        text(u"Зависимость для определения подачи на оборот имеет вид: ")
        form(u'S_О = S_Z * z,')
        text(u"где z - количество зубьев фрезы. Выбранная фреза имеет z = "+dc(str(z))+u" зубьев, поэтому:")
        form(u'S_О = '+dc(str(Sz))+u' * '+dc(str(z))+u' = '+dc(str(So))+u' мм/об.')
    elif type_of_treatment == 2: #чистовая   
        if type_of_milling_cutter == 0 or type_of_milling_cutter == 1 or type_of_milling_cutter == 2 or type_of_milling_cutter == 3:
            #"Дисковая"
            #"Торцовая"
            #"Дисковая, обработка торца"
            #"Дисковая, обработка паза"
            tabl = u"37"
            text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
            form(u'S_Oтабл = '+dc(str(So_tabl))+u' мм/об.')
            text(u"Принимаю: ")
            text(u'S_O = '+dc(str(So))+u' мм/об.', 1)
            text(u"Зависимость для определения подачи на зуб имеет вид: ")
            form(u'S_Z = S_O / z,')
            text(u"где z - количество зубьев фрезы. Выбранная фреза имеет z = "+dc(str(z))+u" зубьев, поэтому:")
            form(u'S_Z = '+dc(str(So))+u' / '+dc(str(z))+u' = '+dc(str(Sz))+u' мм/зуб.')
        elif type_of_milling_cutter == 4 or type_of_milling_cutter == 5 or type_of_milling_cutter == 6 or type_of_milling_cutter == 7 or type_of_milling_cutter == 8 or type_of_milling_cutter == 9:
            #"Отрезная"    #"Расчет не определен, принимаю как для черновой обработки"
            #"Концевая, обработка торца"
            #"Концевая, обработка паза"
            #"Угловая"    #"Расчет не определен, принимаю как для черновой обработки"
            #"Фасонная, с выпуклым профилем"    #"Расчет не определен, принимаю как для черновой обработки"
            #"Фасонная, с вогнутым профилем"    #"Расчет не определен, принимаю как для черновой обработки"  
            if type_of_milling_cutter == 4 or type_of_milling_cutter == 7 or type_of_milling_cutter == 8 or type_of_milling_cutter == 9:
                tabl = u"35"
            else:
                tabl = u"36"
            text(u"Подачу выбираю согласно рекомендациям [10, табл. " + tabl + u"]. Табличное значение подачи: ")
            form(u'S_Zтабл = '+dc(str(Sz_tabl))+u' мм/зуб.')
            text(u"Принимаю: ")
            form(u'S_Zпр = '+dc(str(Sz_take))+u' мм/зуб.')
            text(u"Зависимость для определения подачи на оборот имеет вид: ")
            form(u'S_О = S_Z * z,')
            text(u"где z - количество зубьев фрезы. Выбранная фреза имеет z = "+dc(str(z))+u" зубьев, поэтому:")
            form(u'S_О = '+dc(str(Sz))+u' * '+dc(str(z))+u' = '+dc(str(So))+u' мм/об.')
    #--------------------------------------------------------------------------
    text(u"Период стойкости инструмента: ")
    text(u'T = '+dc(str(T))+u' мм.', 1)
    #--------------------------------------------------------------------------
    text(u"Расчет скорости резания выполняется по эмпирической формуле [10, стр. 282]: ")
    form(u'V = ((C_V * D^q)/(T^m * t^X * S_Z^Y * B^u * z^p)) * K_V,')
    var(u'где K_V - поправочный коэффициент на силу резания: ', u'K_V' )
    form(u'K_V = K_MV * K_PV * K_IV')
    if mat==0 or mat==1 or mat==2:
        var(u'где K_MV - коэффициент, учитывающий влияние материала заготовки: ', u'K_MV')
        form(u'K_MV = K_G * (750/sigv)^(n_V),')
        var(u'где K_G = '+dc(str(KG))+u' - коэффициент, характеризующий группу стали по обрабатываемости; [10, табл. 2]', u'K_G')
        var(u'n_V = ' + dc(str(nV)) + u' - показатель степени; [10, табл. 2]', u'n_V')
        calc(u'K_MV = K_G * (750/sigv)^(n_V)', u' ,', (KMV, KG, sigv, nV))
    elif mat==3:
        var(u'где K_MV - коэффициент, учитывающий влияние материала заготовки: ', u'K_MV')
        form(u'K_MV = (190/HB)^nV,'+ '\n')
        var(u'где n_V = ' + dc(str(nV)) + u' - показатель степени; [10, табл. 2]', u'n_V')
        calc(u'K_MV = (190/HB)^nV', u' ,', (KMV, HB, nV))
    elif mat==4:
        var(u'где K_MV - коэффициент, учитывающий влияние материала заготовки: ', u'K_MV')
        form(u'K_MV = (150/HB)^nV,')
        var(u'где n_V = ' + dc(str(nV)) + u' - показатель степени; [10, табл. 2]', u'n_V')
        calc(u'K_MV = (150/HB)^nV', u' ,', (KMV, HB, nV))
    elif mat==5 or mat==6:
        var(u'где K_MV = '+dc(str(KMV))+u' - коэффициент, учитывающий влияние материала заготовки:', u'K_MV')
    else:
        pass
    var(u'K_PV = '+dc(str(KPV))+u' - коэффициент, учитывающий влияние состояния поверхности заготовки; [10, табл. 5]', u'K_PV')    
    var(u'K_IV = '+dc(str(KIV))+u' - коэффициент, учитывающий влияние состояния поверхности заготовки; [10, табл. 6]', u'K_IV')    
    calc(u'K_V = K_MV * K_PV * K_IV',  u' .', (KV, KMV, KPV, KIV))

    var(u'C_V, Y, m - коэффициент и показатели степеней в формуле резания [10, табл. 39]. ', u'C_V')    
    var(u'C_V = '+dc(str(CV))+u';', u'C_V')
    text(u'q = '+dc(str(q_V))+u';')
    text(u'x = '+dc(str(X_V))+u';')
    text(u'y = '+dc(str(Y_V))+u';')
    text(u'u = '+dc(str(u_V))+u';')
    text(u'p = '+dc(str(p))+u';')
    text(u'm = '+dc(str(m))+u';')
    if type_of_milling_cutter == 1 and V_calc != V:
        text(u"Согласно примечаниям к [10,  табл. 39] скорость резания для торцовых фрез необходимо корректировать в зависимости от главного угла в плане fi. Итоговая зависимости для поределения скорости резания:")
        form(u'V = ((C_V * D^q)/(T^m * t^X * S_Z^Y * B^u * z^p)) * K_V * K_Vfi,')
        var(u'где K_Vfi - поправочный коэффициент, учитывающий величину главного угла в плане fi: ', u'K_Vfi' )
        var(u'K_Vfi = '+dc(str(KVfi))+u';', u'K_Vfi')
        calc(u'V = ((C_V * D^q)/(T^m * t^X * S_Z^Y * B^u * z^p)) * K_V * K_Vfi',  u' м/мин.', (V_calc, CV, dia, q_V, T, m, gr, X_V, Sz, Y_V, B, u_V, z, p, KV, KVfi))
    else:
        calc(u'V = ((C_V * D^q)/(T^m * t^X * S_Z^Y * B^u * z^p)) * K_V',  u' м/мин.', (V_calc, CV, dia, q_V, T, m, gr, X_V, Sz, Y_V, B, u_V, z, p, KV))
    #--------------------------------------------------------------------------
    text(u"После получения расчетных скоростей вычисляется частота вращения шпинделя: ")
    form(u'n_РАСЧ = (1000 * V)/(pi * D),')
    calc(u'n_РАСЧ = (1000 * V)/(pi * dia)',  u' об/мин.', (n_calculated, V, u"3.14", dia))
    #--------------------------------------------------------------------------
    text(u"Рассчитанные значения корректируются по паспорту станка. Принимаем действительное значение частоты вращения: ")
    form(u"n_Д = "+dc(str(n))+u" об/мин")
    #--------------------------------------------------------------------------
    text(u"Действительная скорость резания: ")
    form(u'V_Д = (pi * D * n_Д)/1000,')
    calc(u'V_Д = (pi * D * n)/1000',  u' м/мин.', (V_actual, u"3.14", dia, n))
    #--------------------------------------------------------------------------
    var(u"Определяем составляющую силу резания P_Z по формуле: ", u"P_Z")
    form(u'P_Z = (10 * C_P * t^x * S_Z^y * B^u * z)/(D^q * n^w) * K_MP, ')
    var(u'где C_P, x, y, n - коэффициент и показатели степеней в формуле резания [10, табл. 41]. ', u'C_P', 0)
    var(u'C_P = '+dc(str(CP))+u';', u'C_P', 0)
    var(u'X_P = '+dc(str(X_P))+u';', u'X_P', 0)
    var(u'Y_P = '+dc(str(Y_P))+u';', u'Y_P', 0)
    var(u'u = '+dc(str(u_P))+u';', u'u', 0)
    var(u'q = '+dc(str(q))+u';', u'q', 0)
    var(u'w = '+dc(str(w))+u';', u'w', 0)
    if mat == 0 or mat == 1 or mat == 2 or mat == 3 or mat == 4: 
        var(u'где K_MP - коэффициент, учитывающий влияние качества заготовки [10, табл. 9]. ', u'K_MP')
        if mat == 0 or mat == 1 or mat == 2:
            form(u'K_MP = (sigv/750)^(n_P),')
            var(u'где n_P = ' + dc(str(nP)) + u' - показатель степени; [10, табл. 9]', u'n_P')
            calc(u'K_MP = (sigv/750)^nP',  u',', (KMP, sigv, nP))
        elif mat == 3:
            form(u'K_MP = (HB/190)^(n_P),')
            var(u'где n_P = ' + dc(str(nP)) + u' - показатель степени; [10, табл. 9]', u'n_P')
            calc(u'K_MP = (HB/190)^nP',  u',', (KMP, HB, nP))
        elif mat == 4:
            form(u'K_MP = (HB/150)^(n_P),')
            var(u'где n_P = ' + dc(str(nP)) + u' - показатель степени; [10, табл. 9]', u'n_P')
            calc(u'K_MP = (HB/150)^nP',  u',', (KMP, HB, nP))
    else:
        var(u'где K_MP = '+dc(str(KMP))+u' - коэффициент, учитывающий влияние качества заготовки [10, табл. 10]. ', u'K_MP')
    calc(u'P_Z = (10 * C_P * t^x * S_Z^y * B^u * z)/(D^q * n^w) * K_MP',  u' H.', (Pz, CP, gr, X_P, Sz, Y_P, B, u_P, z, dia, q, n, w, KMP))
    #--------------------------------------------------------------------------
    text(u"Теперь необходимо проверить мощность предварительно выбранного станка. Эффективную мощность, затрачиваемую на резание, рассчитывают по формуле: ")
    form(u"N_рез = (P_Z * V_Д)/(1020 * 60),")
    calc(u"N = (PZ * V)/(1020 * 60)",  u" кВт.", (N, Pz, V_actual, 60, 60)) #TODO: исправить ошибку "tuple index out of range"; разобраться почему надо вводить 2 раза "60"
    text(u"Полученный результат сравнивают с паспортной мощностью: ")
    form(u"N_рез ≤ N_шп")
    form(u"где N_шп = N_ПАС * КПД")
    var(u"N_ПАС = "+dc(str(N_lathe_passport))+u" - мощность шпинделя по паспорту станка; ", u"N_ПАС")
    text(u"КПД = "+dc(str(performance))+u" - коэффициент полезного действия станка; ")
    calc(u"N_шп = N_lathe_passport * performance",  u" кВт,", (N_spindle, N_lathe_passport, performance))
    form(u"N_рез = "+dc(str(N))+u" ≤ N_шп = "+dc(str(N_spindle)))
    #--------------------------------------------------------------------------
    text(u"Остальные составляющие силы резания определяются в соответствии с [10, табл. 42]. ")
    
    text(u"Отношение горизонтальной составляющей силы резания к окружной (главной составляющей): ")
    form(u'P_h/P_Z  = K_Ph = '+dc(str(K_Ph)))
    var(u"Итоговая зависимость для определения горизонтальной силы P_h: ", u"P_h")
    form(u'P_h = K_Ph * P_Z,')
    calc(u'P_h = K_Ph * P_Z',  u' H.', (Ph, K_Ph, Pz))
   
    text(u"Отношение вертикальной составляющей силы резания к окружной (главной составляющей): ")
    form(u'P_v/P_Z  = K_Pv = '+dc(str(K_Pv)))
    form(u'P_v = K_Pv * P_Z,')
    calc(u'P_v = K_Pv * P_Z',  u' H.', (Pv, K_Pv, Pz))
    
    text(u"Отношение радиальной составляющей силы резания к окружной (главной составляющей): ")
    form(u'P_Y/P_Z  = K_PY = '+dc(str(K_Py)))
    form(u'P_Y = K_PY * P_Z,')
    if type_of_milling_cutter == 1 or type_of_milling_cutter == 5 or type_of_milling_cutter == 6:
        text(u"Согласно примечаниям к [10,  табл. 42] итоговое значение радиальной составляющей силы резания необходимо корректировать в зависимости от главного угла в плане. Итоговая зависимость для определения значения радиальной составляющей силы резания: ")
        form(u'P_Y = K_PY * P_Z * K_fi_Py,')
        var(u'где K_fi_Py - поправочный коэффициент, учитывающий величину главного угла в плане fi: ', u'K_fi_Py' )
        var(u'K_fi_Py = '+dc(str(KfiP_Py))+u';', u'K_fi_Py')
        calc(u'P_Y = K_PY * P_Z * K_fi_Py',  u' H.', (Py, K_Py, Pz, KfiP_Py))
    else:
        calc(u'P_Y = K_PY * P_Z',  u' H.', (Py, K_Py, Pz))
    
    text(u"Отношение осевой составляющей силы резания к окружной (главной составляющей): ")
    form(u'P_X/P_Z  = K_PX = '+dc(str(K_Px)))
    form(u'P_X = K_PX * P_Z,')
    if type_of_milling_cutter == 1 or type_of_milling_cutter == 5 or type_of_milling_cutter == 6:
        text(u"Согласно примечаниям к [10,  табл. 42] итоговое значение осевой составляющей силы резания необходимо корректировать в зависимости от главного угла в плане. Итоговая зависимость для определения значения осевой составляющей силы резания: ")
        form(u'P_X = K_PX * P_Z * K_fi_Px,')
        var(u'где K_fi_Px - поправочный коэффициент, учитывающий величину главного угла в плане fi: ', u'K_fi_Px' )
        var(u'K_fi_Px = '+dc(str(KfiP_Px))+u';', u'K_fi_Px')
        calc(u'P_X = K_PX * P_Z * K_fi_Px',  u' H.', (Px, K_Px, Pz, KfiP_Px))
    else:
        calc(u'P_X = K_PX * P_Z',  u' H.', (Px, K_Px, Pz))
    #--------------------------------------------------------------------------   
        
    d.close_a_docx_document()
