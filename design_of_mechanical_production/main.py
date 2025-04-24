#------------------------------------------------------------------------------
# Name:        main                                                          
# Purpose:     Главный модуль программы
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
from inputdata.initial_data import main as initial_data
from processing.calculation import main as processing_data
from output.textfile.to_text_file import main as to_text_file
#------------------------------------------------------------------------------
def input_initial_data():
    # Ввод начальных данных
    # 1) годовой объем выпуска продукции в штуках
    # 2) Датафрейм техпроцесса (с наименованиями и последовательностью операций 
    # и штучным временем для каждой)
    
    input_result = initial_data()

    return input_result


def processing(data):
    # Обработка данных: Расчет количества оборудования, загрузки, рабочих и площадей
    
    processing_result = processing_data(data)

    return processing_result
    

def output_to_textfile(data):
    # Печать в текстовый файл 
    
    is_output_to_file_successful = to_text_file(data)
    
    return is_output_to_file_successful
    

def output_to_kompas(data):
    # Построение планировки цеха в программе КОМПАС 3D 
    
    print ("Модуль вывода в КОМПАС-3D не реализован.")
    
    return False    


#------------------------------------------------------------------------------
def main():
    
    initial_data = input_initial_data()
    
    result = processing(initial_data)
    
    if output_to_textfile(result):
        print ("Вывод в текстовый файл успешно завершен ->")
    else:
        print ("Вывод в текстовый файл не выполнен ->")
        
    # if output_to_kompas(result):
    #     print ("Вывод в файл КОМПАС-3D успешно завершен ->")
    # else:
    #     print ("Вывод в файл КОМПАС-3D не выполнен ->")


#------------------------------------------------------------------------------
if __name__ == "__main__":
    main()