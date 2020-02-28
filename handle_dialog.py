#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from add_recipe import *

def handle_dialog(request, response, user_storage, db):
    if request.is_new_session:
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        response.set_text("Выберите действие")
        response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}
                    ])
        return response, user_storage
    else:
        if request.command.lower() == "добавь рецепт":
            user_storage["add recipe"] = 1
            response.set_text("Скажите название рецепта")
            return response, user_storage
        elif user_storage["add recipe"] > 0:
            response, user_storage = add_recipe(request, response, user_storage, db)
            return response, user_storage
        elif request.command.lower() == "удали рецепт":
            user_storage["delete recipe"] = 1
            response.set_text("Скажите название рецепта для удаления")
            return response, user_storage
        elif user_storage["delete recipe"] == 1:
            user_storage["delete recipe"] = 0
            delete_db(db, request.user_id, request.command.lower())
            response.set_text("Рецепт успешно удален")
            return response, user_storage
        else:
            response.set_text("Неизвестное действие, выберите то, что есть")
            response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}])
            return response, user_storage
'''            response.set_text("До встречи!")
            response.set_end_session(True)
            user_storage = {}
            return response, user_storage
        return response, user_storage'''
'''        elif request.command.lower() == "покажи в бд":
            user_storage[1] = 1
            response.set_text("Ок!")
            return response, user_storage
        elif user_storage[1] == 1:
            user_storage[1] = 0
            doc = get_recipe(db, request.user_id, request.command)
            response.set_text(doc["name"])
            return response, user_storage'''
