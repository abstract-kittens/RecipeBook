#! /usr/bin/env python
# -*- coding: utf-8 -*-
import db_api

def show_recipe(request, response, user_storage, db):
    if request.command.lower() == "отменить":
        response.set_text("Хорошо, запускаю отмену...")
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "calculator" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        return response, user_storage
        
    elif user_storage["get recipe"] == 1:
        user_storage["name"] = request.command.lower()
        if db_api.get_db(db, request.user_id, user_storage["name"]) == None:
            response.set_text("""Я не знаю этот рецепт""")
        else:
            response.set_text("""что вы хотите услышать: список ингрендиентов 
                          или шаги приготовления?""")
            user_storage["get recipe"] = 2
        return response, user_storage
    
    elif user_storage["get recipe"] == 2:
        if request.command.lower() == "ингредиенты":
            rez = db_api.get_db(db, request.user_id, user_storage["name"])
            s = ""
            for i in rez['ingredients']:
                s += ' '.join(i) + '\n'
            response.set_text(s + ". Хотите узнать что-то еще?")
            user_storage["get recipe"] = 3
            return response, user_storage
        
        elif request.command.lower() == "шаги":
            rez = db_api.get_db(db, request.user_id, user_storage["name"])
            rez = ','.join(rez['steps'])
            response.set_text(rez + ". Хотите узнать что-то еще?")
            user_storage["get recipe"] = 3
            return response, user_storage
        else:
            response.set_text("Я вас не поняла")
            return response, user_storage
   
    elif user_storage["get recipe"] == 3:
        if request.command.lower() == "нет":
            response.set_text("Хорошо, запускаю отмену...")
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
            return response, user_storage
        elif request.command.lower() == "да":
            response.set_text("""что вы хотите услышать: список ингрендиентов 
                          или шаги приготовления?""")
            user_storage ["get recipe"] = 2
            return response, user_storage
        else: 
            response.set_text("""Я вас не поняла""")
            return response, user_storage
    elif request.command.lower() == "":
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "calculator" : 1,"ingredients":None,
                        "steps" : None}
    else: 
        response.set_text("Я вас не поняла")
        return response, user_storage