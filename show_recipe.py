#! /usr/bin/env python
# -*- coding: utf-8 -*-
import db_api
from calculator import *

def show_recipe(request, response, user_storage, db):
    if request.command.lower() in [
            "отменить",
            'отмена',
            'назад'
            ]:
        response.set_text("Можете выбрать другое действие над рецептом")
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "calculator" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Пересчитай рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}])
        return response, user_storage
        
    elif user_storage["get recipe"] == 1:
        user_storage["name"] = request.command.lower()
        if db_api.get_db(db, request.user_id, user_storage["name"]) == None:
            response.set_text("""Я не знаю этот рецепт""")
        else:
            response.set_text("""что вы хотите услышать: список ингредиентов 
                          или шаги приготовления?""")
            user_storage["get recipe"] = 2
        return response, user_storage
    elif user_storage["get recipe"] == 2:
        if request.command.lower() in [
            'ингредиент',
            'список',
            'список ингредиентов',
            'ингредиенты',
            ]:
            rez = db_api.get_db(db, request.user_id, user_storage["name"])
            s = ""
            for i in rez['ingredients']:
                s += ' '.join(i) + '\n'
            response.set_text(s + ". Хотите узнать что-то еще?")
            user_storage["get recipe"] = 3
            return response, user_storage
        
        elif request.command.lower() in [
            'шаг',
            'список шагов',
            'этапы',
            'этапы приготовления'
            ]:
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
            response.set_text("Можете выбрать другое действие над рецептом")
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                         "calculator" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
            response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Пересчитай рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}])
            return response, user_storage
        elif request.command.lower() == "да":
            response.set_text("""что вы хотите услышать: список ингредиентов 
                          или шаги приготовления?""")
            user_storage ["get recipe"] = 2
            return response, user_storage
        else: 
            response.set_text("""Я вас не поняла""")
            return response, user_storage
    else: 
        response.set_text("Я вас не поняла")
        return response, user_storage