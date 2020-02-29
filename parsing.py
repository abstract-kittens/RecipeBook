#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

#s = """куриное филе 500 грамм жопы единорогов 8 штук помидор 1 штука молоко 200 миллилитров
#        сахар 2 чайных ложки соль и перец по вкусу корица 1 столовая ложка"""
def morphy(item):
    forms = morph.parse(item)
    forms = forms[0].normal_form
    return forms

def parser_ingred(s):
    names = []
    mass = []
    mer  = []
    rez = []
    name = ""
    merName = ""
    lastitem = ""
    s = s.split()
    
    for item in s:
        
        if (item.isnumeric() == True):
            mass.append(item)
            names.append(name.rstrip())
            name = ""
            
        else:
            if(morphy(item) != "ложка"):
                name += item + " "        
                
            if(lastitem.isnumeric() == True):
                if (morphy(item) == "чайный"):
                    item = "чайная ложка"
                elif (morphy(item) == "столовый"):
                    item = "столовая ложка"
                mer.append(morphy(item))
                name=""
                
            elif(lastitem == "по" and item == "вкусу"):
                mass.append('0')
                merName = lastitem + " " + item
                mer.append(merName)
                names.append(name.replace('по вкусу', '').rstrip())
                name=""
                merName="" 
        lastitem = item 
    i = 0
    while i < len(names):
        rez.append([names[i], mass[i], mer[i]])
        i += 1
    return rez
#    print(rez)

#s = "шаг 1 возьмите гнома шаг 2 отрежте гному жопу шаг 3 повторите шаг 1 и добавьте больше жоп в блюдо" 
def parser_step(s):
    rez = []
    number = 1
    temp = ""
    
    s = s.split();
    for i in range(len(s)):
        if(s[i] == "шаг" and s[i+1] == str(number)):
            if(temp != ''):
                rez.append(temp.rstrip())
            temp = ""
#            print(temp, number)
        elif (s[i-1] == "шаг" and s[i] == str(number)):
            number += 1 
        else:
            temp += s[i] + " "
            #print(temp)
    rez.append(temp.rstrip())
    return rez
#    print(rez)
        
        
    
    
#parser_step(s)    
#parser_ingred(s)
        