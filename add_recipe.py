#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import parsing
import db_api

def add_recipe(request, response, user_storage, db):
    if request.command.lower() in [
            "отменить",
            'отмена',
            'назад'
            ]:
        response.set_text("Можете выбрать другое действие над рецептом, либо прослушать помощь")
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Пересчитай рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}
                    ])
        return response, user_storage
    
    elif user_storage["add recipe"] == 1:
        if db_api.get_db(db, request.user_id, request.command.lower()):
            response.set_text("Такой рецепт уже существует. Чтобы добавить рецепт с дргуим именем введите \"добавить рецепт\"")
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
            return response, user_storage
        user_storage["name"] = request.command.lower()
        response.set_text("Назови ингредиенты в формате " +
                          "[название ингредиента] [количество] [мера]")
        user_storage["add recipe"] = 2
        return response, user_storage
    
    elif user_storage["add recipe"] == 2:
        if user_storage["ingredients"]:
            user_storage["ingredients"] = (user_storage["ingredients"] +
                            parsing.parser_ingred(request.command.lower()))
        else:
            user_storage["ingredients"] = parsing.parser_ingred(request.command.lower())
        response.set_text("Хотите добавить еще ингредиенты? (да/нет)")
        user_storage["add recipe"] = 3
        return response, user_storage
    
    elif user_storage["add recipe"] == 3:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 2
            response.set_text = response.set_text("Назови ингредиенты в " +
                        "формате [название ингредиента] [количество] [мера]")
        elif request.command.lower() == "нет":
            user_storage["add recipe"] = 4
            response.set_text = response.set_text("Хотите назвать шаги приготовления?")
        else:
            user_storage["edit recipe"] = 3
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["add recipe"] == 4:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 5
            response.set_text = response.set_text("Назови шаги в формате " +
                        "Шаг 1 [описание шага] Шаг 2 [описание шага]")
        elif request.command.lower() == "нет":
            db_api.add_db(db, request.user_id, user_storage["name"],
                          user_storage["ingredients"], user_storage["steps"])
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
            response.set_text = response.set_text("Спасибо, рецепт добавлен!")
        else:
            user_storage["edit recipe"] = 4
            response.set_text("Неизвестная команда. Хотите повторить ввод?")
        return response, user_storage
    
    elif user_storage["add recipe"] == 5:
        if user_storage["steps"]:
            user_storage["steps"] = user_storage["steps"] + parsing.parser_step(request.command.lower())
        else:
            user_storage["steps"] = parsing.parser_step(request.command.lower())
        response.set_text = response.set_text("Хотите добавить еще шаги приготовления?")
        user_storage["add recipe"] = 4
        return response, user_storage