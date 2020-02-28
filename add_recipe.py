#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import parsing
import db_api

#s = """фелиное куре 500 грамм масло 120 грамм помидор 1 штука 
#        соль по вкусу жопа гнома 2 киллограмма"""
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
            name += item + " "            
            if(lastitem.isnumeric() == True):
                forms = morph.parse(item)
                mer.append(forms[0].normal_form)
                name=""
                
            elif(lastitem == "по" and item == "вкусу"):
                mass.append('0')
                merName = lastitem + " " + item
                mer.append(merName)
                name=""
                merName="" 
        lastitem = item 
    i = 0
    while i < len(names):
        rez.append([names[i], mass[i], mer[i]])
        i += 1
    return rez
    #print(rez)

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
            temp = "Шаг "
#            print(temp, number)
            number += 1  
        else:
            temp += s[i] + " "
            #print(temp)
    rez.append(temp.rstrip())
    return rez
#    print(rez)
 
def add_recipe(request, response, user_storage, db):
    if request.command.lower() == "отменить":
        response.set_text("Хорошо, запускаю отмену...")
        user_storage = {"add recipe" : 0, "get recipe" : 0}
        return response, user_storage
    elif user_storage["add recipe"] == 1:
        user_storage["name"] = request.command.lower()
        response.set_text("Назови ингредиенты в формате [название ингредиента] [количество] [мера]")
        user_storage["add recipe"] = 2
        return response, user_storage
    elif user_storage["add recipe"] == 2:
        user_storage["ingredients"] = user_storage["ingredients"] + parsing.parser_ingred(request.command.lower())
        #k = add_recipe(db, request.user_id, request.command)
        response.set_text("Хотите добавить еще ингредиенты? (да/нет)")
        user_storage["add recipe"] = 3
        return response, user_storage
    elif user_storage["add recipe"] == 3:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 2
            response.set_text = response.set_text("Назови ингредиенты в формате [название ингредиента] [количество] [мера]")
        elif request.command.lower() == "нет":
            user_storage["add recipe"] = 4
            response.set_text = response.set_text("Хотите назвать шаги приготовления?")
        return response, user_storage
    elif user_storage["add recipe"] == 4:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 5
            response.set_text = response.set_text("Назови шаги в формате Шаг 1 [описание шага] Шаг 2 [описание шага]")
        elif request.command.lower() == "нет":
            db_api.add_db(db, request.user_id, user_storage["name"], user_storage["ingredients"], user_storage["steps"])
            user_storage = {"add recipe" : 0, "get recipe" : 0}
            response.set_text = response.set_text("Спасибо, рецепт добавлен!")
        return response, user_storage
    elif user_storage["add recipe"] == 5:
        user_storage["steps"] = user_storage["steps"] + parsing.parser_step(request.command.lower())
        response.set_text = response.set_text("Хотите назвать шаги приготовления?")
        user_storage["add recipe"] = 4
        return response, user_storage