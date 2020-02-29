#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from db_api import *
import parsing
from find_one import *

def edit_recipe(request, response, user_storage, db):
    if request.command.lower() == "отменить":
        response.set_text("Хорошо, запускаю отмену...")
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        return response, user_storage
    
    elif user_storage["edit recipe"] == 1:
        user_storage["edit recipe"] = 2
        doc = get_db(db, request.user_id, request.command.lower())
        if doc != None:
            user_storage["ingredients"] = doc["ingredients"]
            user_storage["steps"] = doc["steps"]
            user_storage["name"] = request.command.lower()
            response.set_text("Что вы хотите изменить? (название/ингредиенты/шаги)")
        else:
            response.set_text("Такого рецепта нет. Изменение не может быть выполнено")
            user_storage["edit recipe"] = 0
        return response, user_storage
    
    elif user_storage["edit recipe"] == 2:
        if (request.command.lower() == "название"):
            user_storage["edit recipe"] = 3
            response.set_text("На какое имя хотите изменить?")
        elif (request.command.lower() == "ингредиенты"):
            user_storage["edit recipe"] = 9
            response.set_text("Хотите удалить или добавить ингредиент?")
        elif (request.command.lower() == "шаги"):
            user_storage["edit recipe"] = 4
            response.set_text("Хотите удалить или добавить шаги?")
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 3:
        update_name_db(db, request.user_id, user_storage["name"], request.command.lower())
        response.set_text("Хотите изменить что-то еще в этом рецепте?")
        user_storage["edit recipe"] = 100
        return response, user_storage
    
    elif user_storage["edit recipe"] == 4:
        if request.command.lower() == "удалить":
            response.set_text("Какой шаг " + request.command.lower() + "?")
            user_storage["edit recipe"] = 5
        elif request.command.lower() == "добавить":
            response.set_text("Какой шаг " + request.command.lower() + "?")
            user_storage["edit recipe"] = 6
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 5:
        step = int(request.command.lower())
        if step > len(user_storage["steps"]) or 0 > step:
            user_storage["edit recipe"] = 8
            response.set_text("Номер невалидный. Хотите повторить ввод номера шага?")
        else:
            del user_storage["steps"][step - 1]
            update_steps_db(db, request.user_id, user_storage["name"], user_storage["steps"])
            user_storage["edit recipe"] = 100
            response.set_text("Удалено. Хотите изменить что-то еще в этом рецепте?")
        return response, user_storage
       
    elif user_storage["edit recipe"] == 6:
        user_storage["step"] = int(request.command.lower()) - 1
        if user_storage["step"] >= len(user_storage["steps"]):
            user_storage["step"] = len(user_storage["steps"]) - 1
        response.set_text("Продиктуйте шаг")
        user_storage["edit recipe"] = 7
        return response, user_storage
        
    elif user_storage["edit recipe"] == 7:
        user_storage["steps"].insert(user_storage["step"], request.command.lower())
        update_steps_db(db, request.user_id, user_storage["name"], user_storage["steps"])
        user_storage["edit recipe"] = 100
        response.set_text("Добавлено. Хотите изменить что-то еще в этом рецепте?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 8:
        if request.command.lower() == "да":
            response.set_text("Какой шаг удалить?")
            user_storage["edit recipe"] = 5
        elif request.command.lower() == "нет":
            user_storage["edit recipe"] = 100
            response.set_text("Хотите изменить что-то еще в этом рецепте?")
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
  
    elif user_storage["edit recipe"] == 9:
        if request.command.lower() == "удалить":
            response.set_text("Какой ингредиент " + request.command.lower() + "?")
            user_storage["edit recipe"] = 10
        elif request.command.lower() == "добавить":
            user_storage["edit recipe"] = 11
            response.set_text("Какой ингредиент " + request.command.lower() + "?")
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 10:
        step = find_ingr(user_storage["ingredients"], request.command.lower())
        if step == -1:
            user_storage["edit recipe"] = 13
            response.set_text("Такого ингредиента нет. Хотите повторить ввод?")
        else:
            del user_storage["ingredients"][step]
            update_steps_db(db, request.user_id, user_storage["name"], user_storage["steps"])
            user_storage["edit recipe"] = 100
            response.set_text("Удалено. Хотите изменить что-то еще в этом рецепте?")
        return response, user_storage
 
    elif user_storage["edit recipe"] == 11:
        response.set_text("Продиктуйте игредиенты в формате [название ингредиента] [количество] [мера]")
        user_storage["edit recipe"] = 12
        return response, user_storage
        
    elif user_storage["edit recipe"] == 12:
        user_storage["ingredients"] = (user_storage["ingredients"] +
                    parsing.parser_ingred(request.command.lower()))
        update_ingredients_db(db, request.user_id, user_storage["name"], user_storage["ingredients"])
        user_storage["edit recipe"] = 100
        response.set_text("Добавлено. Хотите изменить что-то еще в этом рецепте?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 13:
        if request.command.lower() == "да":
            response.set_text("Какой ингредиент удалить?")
            user_storage["edit recipe"] = 10
        elif request.command.lower() == "нет":
            user_storage["edit recipe"] = 100
            response.set_text("Хотите изменить что-то еще в этом рецепте?")
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["edit recipe"] == 100:
        if request.command.lower() == "да":
            user_storage["edit recipe"] = 2
            response.set_text("Что вы хотите изменить? (название/ингредиенты/шаги)")
        elif request.command.lower() == "нет":
            user_storage = {"add recipe" : 0, "get recipe" : 0,
            "delete recipe" : 0, "edit recipe" : 0,
            "name" : None, "ingredients":None,
            "steps" : None}
            response.set_text("Изменения произведены")
        else:
            user_storage["edit recipe"] = 100
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage