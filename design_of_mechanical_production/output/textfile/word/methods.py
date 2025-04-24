#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Output to file *.docx calculation of cutting modes
# Purpose:     Print the calculated data to a report
#
# Author:      ANKorenuk
#
# Created:     01.01.2020
# Copyright:   (c) ANKorenuk 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
import os
import win32com.client
import re # для вывода расчета в формулу

import pandas as pd

# Для замены точки на запятую
try:
    from string import maketrans   # Python 2
except ImportError:
    maketrans = str.maketrans      # Python 3

#------------------------------------------------------------------------------
class OutputDataToDocx:
    def __init__(self, parent=None, filename=None):
        self.create_a_new_name(filename)
        
        self.COM_WORD_object = win32com.client.Dispatch('Word.Application')
        
        self.name = self.COM_WORD_object.Documents.Add()
            
        self.name.SaveAs2(self.faledir)
        self.COM_WORD_object.Application.Keyboard (1049)
        self.COM_WORD_object.Application.Visible = True
        
        self.FONT = "Times New Roman"
        self.SIZE = 14
        self.LINESPACING = 12
        self.ALIGNMENT = 3
        self.TEXT_ALIGNMENT = self.ALIGNMENT
        
        self.set_text_settings("Times New Roman", 14, 12, 3)
        
        
    def create_a_new_name(self, filename):
        if not isinstance(filename, type(None)): 
            self.filename = filename
            self.curdir = os.path.abspath(os.curdir)
            self.faledir = self.curdir +'\\' + self.filename
        else:
            self.curdir = os.path.abspath(os.curdir)
            self.now = datetime.datetime.now()
            self.filename = 'report ' + self.now.strftime('%H-%M %d-%m-%Y') + ''
            self.faledir = self.curdir +'\\' + self.filename 
        
        
    def save_a_docx_document(self):
        self.name.Save()
    
    
    def close_a_docx_document(self):
        self.name.Save()
        self.name.Close()
        self.COM_WORD_object.Quit()
        print ('Вывод в файл ' + str(self.filename) + '.docx -> Выполнено (с сохранением) ->')
        
        
    def set_text_settings(self, FONT, SIZE, LINESPACING, ALIGNMENT):
        """
        Задаем параметры глобального форматирования
        
        Argvs:
        FONT - Шрифт
        SIZE - Размер
        LINESPACING - Межстрочный интервал
        ALIGNMENT - выравнивание (0-3, где 0- по левому краю, ..., 3 - по ширине)
        """
        self.COM_WORD_object.Selection.Font.Name = FONT
        self.COM_WORD_object.Selection.Font.Size = SIZE
        self.COM_WORD_object.Selection.ParagraphFormat.LineSpacing = LINESPACING
        self.COM_WORD_object.Selection.ParagraphFormat.Alignment = ALIGNMENT
    
        
    def output_a_string_in_docx(self, string, TEXT_ALIGNMENT=3):
        """
        Выводит строку текста
        
        Argvs:
        string - строка c выводимым текстом
        TEXT_ALIGNMENT - выравнивание строки
        """
        string = self.get_str(string)
        string_correct = string + "\n"
        string_correct = self.get_str(string_correct)
        self.COM_WORD_object.Selection.TypeParagraph
        self.COM_WORD_object.Selection.ParagraphFormat.Alignment = TEXT_ALIGNMENT
        self.COM_WORD_object.Selection.TypeText(string_correct)  
        
    
    def output_a_formula_in_docx(self, formula):
        """
        Преобразует text в математическую формулу
        
        Argvs:
        formula - строковая последовательность, котрую нужно напечатать в виде 
        формулы
        """
        formula = self.get_str(formula)
        self.COM_WORD_object.Selection.TypeBackspace
        objRange = self.COM_WORD_object.Selection.Range 
        objRange.Text = formula
        objRange = self.COM_WORD_object.Selection.OMaths.Add(objRange) 
        objEq = objRange.OMaths(1)
        objEq.BuildUp()
        self.COM_WORD_object.Selection.EndKey(5, 0)
        self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=1)
        self.COM_WORD_object.Selection.TypeText('\n')  
    
    
    def output_text_with_the_variable_name(self, text, name_variable, TEXT_ALIGNMENT=3):
        """
        Выводит имя переменной
        
        Argvs:
        name_variable - строка c выводимым именем переменной
        """
        text_correct = self.get_str(text) + "\n"
        list_text_correct = text_correct.split(name_variable)
        
        self.COM_WORD_object.Selection.TypeParagraph
        if len(list_text_correct)>1:
            self.COM_WORD_object.Selection.ParagraphFormat.Alignment = TEXT_ALIGNMENT
            for i in range(len(list_text_correct) - 1):
                self.COM_WORD_object.Selection.TypeText(list_text_correct[i])
                self.COM_WORD_object.Selection.TypeBackspace
                self.COM_WORD_object.Selection.TypeBackspace
                objRange = self.COM_WORD_object.Selection.Range 
                objRange.Text = name_variable
                objRange = self.COM_WORD_object.Selection.OMaths.Add(objRange) 
                objEq = objRange.OMaths(1)
                objEq.BuildUp()
                self.COM_WORD_object.Selection.EndKey(5, 0)
                self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=1)
                
            # self.COM_WORD_object.Selection.ParagraphFormat.Alignment = TEXT_ALIGNMENT
            self.COM_WORD_object.Selection.TypeText(list_text_correct[-1])
        else:
            self.COM_WORD_object.Selection.TypeBackspace
            self.COM_WORD_object.Selection.TypeBackspace
            objRange = self.COM_WORD_object.Selection.Range 
            objRange.Text = name_variable
            objRange = self.COM_WORD_object.Selection.OMaths.Add(objRange) 
            objEq = objRange.OMaths(1)
            objEq.BuildUp()
            self.COM_WORD_object.Selection.EndKey(5, 0)
            self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=1)
            self.COM_WORD_object.Selection.ParagraphFormat.Alignment = TEXT_ALIGNMENT
            self.COM_WORD_object.Selection.TypeText(list_text_correct[0])
            
        
    def output_of_calculations_in_docx(self, formula, dimension, data):
        """
        Печатает расчет формулы как математическую формулу
        по крайней мере, должен...
        
        Argvs:
        formula - строка с формулой
        data - список значений в формуле (float) в порядке следования в formula
        dimension - размерность
        
        !!!Затея не удалась - расчет формулы печатаю как обычную формулу с 
        применением f"" строк
        """
        list_value = re.findall(r"[\w.\w]+", formula)
        #list_value = re.split(r"[\^/=()*,\.]+", formula)
        for i in range(0, len(list_value)):
            try:
                if self.is_number(list_value[i]) == True:
                    list_value.pop(i)
                    i = i + 1 
            except IndexError:pass
            
        edit_formula = formula
        for i in range(1, len(list_value)):
            edit_formula = edit_formula.replace(list_value[i], self.dot_comma(data[i]))
        self.output_a_formula_in_docx(edit_formula)
        self.COM_WORD_object.Selection.MoveLeft(Unit = 1, Count = 2)
        self.output_a_string_in_docx(' = ' + self.dot_comma(data[0]) + ' ' + str(dimension))
    
    
    def dot_comma(self, float_val):
        """
        Заменяет точку у значений float переменных на запятую при печати в строку.
        
        Argvs:
        float_val - значение типа float
        
        Возвращает строку типа str
        """
        float_val = str(float_val)
        str_val = max(float_val.replace('.',',').split())
        return (str_val)
    
    
    def is_number(self, str):
        """
        Проверяет число ли str
        """
        try:
            float(str)
            return True
        except ValueError:
            return False
            
    
    def sym(self, name):
        #TODO: блок ввода символов
        
        if name == '*':
            name = self.COM_WORD_object.Selection.InsertSymbol(42,"Times New Roman", True)
            symvol = self.COM_WORD_object.Selection.InsertSymbol(903,"Times New Roman", True) #знак умножения (точка)
        
        self.COM_WORD_object.Selection.MoveLeft (Unit = 4, Count = 1)
        self.COM_WORD_object.Selection.OMaths(1).ConvertToNormalText
        self.COM_WORD_object.Selection.Find.ClearFormatting
        self.COM_WORD_object.Selection.Find.Replacement.ClearFormatting
        
        self.COM_WORD_object.Selection.Find.text = "*"
        self.COM_WORD_object.Selection.Find.Replacement.text = symvol
        self.COM_WORD_object.Selection.Find.Forward = True
        self.COM_WORD_object.Selection.Find.Wrap = 2
        self.COM_WORD_object.Selection.Find.Format = True
        self.COM_WORD_object.Selection.Find.MatchCase = False
        self.COM_WORD_object.Selection.Find.MatchWholeWord = False
        self.COM_WORD_object.Selection.Find.MatchWildcards = False
        self.COM_WORD_object.Selection.Find.MatchSoundsLike = False
        self.COM_WORD_object.Selection.Find.MatchAllWordForms = False
        
        self.COM_WORD_object.Selection.Find.Execute (Replace = 2)
        self.COM_WORD_object.Selection.OMaths(1).ConvertToMathText
        self.COM_WORD_object.Selection.MoveRight (Unit = 4, Count = 1)
        
        
    def output_table_in_docx(self, table):
        """
        Создает таблицу с размерами table. Печатает таблицу с данными из table.
        Берет кажде значение из ячейки table, переводит в строку, заменяет 
        символы в строке по правилам get_str(), печатает в соответствующую 
        ячейку таблицы документа

        Parameters
        ----------
        table : DataFrame
            DataFrame-таблица для вывода в документ.

        Returns
        -------
        None.

        """
        numrows = len(table.index)
        numcolumns = len(table.columns)
        
        self.COM_WORD_object.Selection.TypeParagraph
        objRange = self.COM_WORD_object.Selection.Range 
        
        tab = self.COM_WORD_object.Selection.Tables.Add(objRange, 
                                                        NumRows = numrows, 
                                                        NumColumns = numcolumns)
        tab.AllowAutoFit = True
        tab.AutoFormat(Format = 16)
        tab.AutoFitBehavior(1)
        
        for rowIndex, row in table.iterrows():
            for columnIndex, value in row.items():
                cell = tab.Cell(rowIndex + 1, columnIndex + 1)
                cell.VerticalAlignment = 1
                cell.WordWrap = True
                cell.Select()
                self.COM_WORD_object.Selection.ParagraphFormat.Alignment = 1
                if isinstance(value, type(None)):
                    cell.Range.Text = ""
                else:
                    value = self.get_str(value)
                    if str(value).find("_") != -1 or str(value).find("^") != -1 or str(value).find("/") != -1:
                        objRange = self.COM_WORD_object.Selection.Range 
                        objRange.Text = value
                        objRange = self.COM_WORD_object.Selection.OMaths.Add(objRange) 
                        objEq = objRange.OMaths(1)
                        objEq.BuildUp()
                        self.COM_WORD_object.Selection.EndKey(5, 0)
                        self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=1)
                    else:
                        cell.Range.Text = value
                
        tab.AutoFitBehavior(2)
        self.COM_WORD_object.Selection.EndKey(5, 0)
        self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=2)
    
    
    def numbered_formula_in_table(self, formula:str, number:str):
        """
        Выводит нумерованную формулу.
        Создает таблицу с прозрачными границами с одной строкой из двух ячеек.
        В первую ячейку пишет формуру "formula" по правилам и с настройками 
        из функции output_a_formula_in_docx(); во вторую - пишет номер формулы 
        "number".

        Parameters
        ----------
        formula : str
            Строка для вывода в формулу.
        number : str
            номер формулы.

        Returns
        -------
        None.

        """
        formula = self.get_str(formula)
        
        self.COM_WORD_object.Selection.TypeParagraph
        objRange = self.COM_WORD_object.Selection.Range 
        tab = self.COM_WORD_object.Selection.Tables.Add(objRange, 
                                                        NumRows = 1, 
                                                        NumColumns = 2)
        tab.Columns(2).PreferredWidthType = 2
        tab.Columns(2).PreferredWidth = 5
        tab.Columns(1).PreferredWidthType = 2
        tab.Columns(1).PreferredWidth = 95
        tab.AllowAutoFit = True
        
        cell = tab.Cell(1, 1)
        cell.VerticalAlignment = 1
        cell.WordWrap = True
        cell.Select()
        self.output_a_formula_in_docx(formula)
        self.COM_WORD_object.Selection.TypeBackspace()
        self.COM_WORD_object.Selection.ParagraphFormat.Alignment = 1
        
        cell = tab.Cell(1, 2)
        cell.Range.Text = str(number)
        cell.VerticalAlignment = 1
        cell.WordWrap = True
        cell.Select()
        
        self.COM_WORD_object.Selection.ParagraphFormat.Alignment = 1
        self.COM_WORD_object.Selection.MoveRight(Unit=1, Count=2)
        # self.output_a_string_in_docx('')
        
        
    def get_str(self, character_string):
        """
        Заменяет символы в строке вывода. Например заменяет "*" на "∙", 
        "СУМ" на "∑", и др. Также, заменяет точку в числах на запятую.

        Parameters
        ----------
        character_string : str, int, float
            Строка, в которой содержаться символы для замены.

        Returns
        -------
        character_string : TYPE
            Строка с замененными символами.

        """
        character_string = str(character_string)
        
        # заменяем символы
        symbols_to_replace = {"*": "∙",
                              "СУМ": "∑",
                              }
        for key, value in symbols_to_replace.items():
            if character_string.find(key) != -1:
                character_string = character_string.replace(key, value)
        
        # заменяет точку в числах на запятую
        swaps = re.findall(r"\d+.\d+", character_string)
        for swap in swaps:
            swap_new = swap.replace(".", ",")
            character_string = character_string.replace(swap, swap_new)

        return character_string
        
        
        
if __name__ == '__main__':
    
    app = OutputDataToDocx(filename="001")
    app.output_a_string_in_docx('Какая-то строка. ')
    app.output_a_string_in_docx('Воооооооооозмоооооооооожноооооооооо, оооооооооочеееееееееень длииииииииииннааааааааааяяяяяяяяяя')
    app.output_a_formula_in_docx('V=(C_V * K_V)/(T^m * S^Y)') 
    app.output_a_string_in_docx('')
    app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(1)") 
    app.output_a_string_in_docx('')
    app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(01)") 
    app.output_a_string_in_docx('')
    app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(001)") 
    app.output_a_string_in_docx('')
    app.output_of_calculations_in_docx('V=(C_V * K_V)/(T^m * S^Y)', 'м/мин', (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0))
    app.output_text_with_the_variable_name('где K_MV - имя переменной. ', 'K_MV')
    T_take = "60.0"
    Kr = 0.94
    T = 56.4
    app.output_of_calculations_in_docx('T = '+T_take+' * Kr ',  ' .', (T, Kr))
    
    app.output_text_with_the_variable_name('где t_g – трудоёмкость детале-операции, ч.;', 't_g')
    complexity_norm = 40
    app.output_text_with_the_variable_name(f't_g = {complexity_norm} н-ч.;', 't_g')
    app.output_a_string_in_docx("N – годовой объём выпуска;")
    annual_output_volume = 365.258
    app.output_a_string_in_docx(f"N = {annual_output_volume} шт.;")
    app.output_text_with_the_variable_name('П_ОП – процентное содержание операции, %.', 'П_ОП')
    
    # data = pd.DataFrame({ 
    #     0 : [              "005",             "010",               "015",             "020", ],
    #     1 : [   "Токарная с ЧПУ", "Расточная с ЧПУ",    "Токарная с ЧПУ", "Фрезерная с ЧПУ", ],
    #     2 : [        "42.69^2_3",       "76.16_3^2",               20.66,               6.8, ],
    #     3 : ["DMG CTX beta 2000",    "УЦИ 2431СФ10", "DMG CTX beta 2000",  "DMG DMU 80 eVo", ],
    # })
    # app.output_table_in_docx(data)
    # app.output_a_string_in_docx('')
    # app.output_table_in_docx(data)
    
    # app.output_a_string_in_docx('')
    # app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(1)")
    # app.output_a_string_in_docx('')
    
    # app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(10)")
    # app.output_a_string_in_docx('')
    
    # app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(100)")
    # app.output_a_string_in_docx('')
    
    # app.numbered_formula_in_table('V=(C_V * K_V)/(T^m * S^Y)', "(1000)")
    # app.output_a_string_in_docx('')
    
    # app.output_a_string_in_docx('Какая-то строка. ')
    # app.output_a_string_in_docx('')
    # app.output_text_with_the_variable_name('где t_g – трудоёмкость детале-операции, ч., t_g = значение по умолчанию', 't_g')
    
    app.close_a_docx_document()

          
        
        
        
        