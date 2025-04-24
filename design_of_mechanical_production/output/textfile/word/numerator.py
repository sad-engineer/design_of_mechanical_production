#------------------------------------------------------------------------------
# Name:        numerator                                                          
# Purpose:     Счетчик
#              
# Author:      ANKorenuk                                                        
#                                                                               
# Created:     16.11.2021                                                       
# Copyright:   (c) ANKorenuk 2021                                               
# Licence:     <your licence>                                                   
#------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------

class numerator():
    """
    При первом вызыве отдает 0. 
    При каждом последующем вывыве, возвращает на 1 больше. 
    Для старта с какого либо числа Х - присвоить numerator().number = Х - 1
    """
    
    def __init__(self, number=0, prefix = "", suffix=""):
        self.number = number
        self.suffix = suffix
        self.prefix = prefix
        
    def __call__(self):
        
        self.number += 1
        self.result = str(self.prefix) + str(self.number) + str(self.suffix)
        return self.result