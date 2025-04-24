#------------------------------------------------------------------------------
# Name:        to_text_file                                                          
# Purpose:     Модуль вывода данных в текстовый файл
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

TYPE_TEX_FILE = "WORD"
#------------------------------------------------------------------------------

def main(data=None):
     # Печать в текстовый файл
     
    if TYPE_TEX_FILE == "WORD":
        from output.textfile.word.to_word import main as output
        result = output(data)
        
    else:
        result = True
        print ("Модуль вывада в текстовый файл не реализован.")
        
    return result


if __name__ == "__main__":
    main()