#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from add_recipe import *
from edit_recipe import *
from show_recipe import *
from calculator import *

def handle_dialog(request, response, user_storage, db):
    if request.is_new_session:
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "calculator" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        response.set_text("Выберите действие")
        response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Пересчитай рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}
                    ])
        return response, user_storage
    else:
        if request.command.lower() == "выйти":
            response.set_text("Спасибо за визит!")
            response.set_end_session(True)
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
            return response, user_storage
        elif request.command.lower() in [
                "добавь рецепт",
                'запиши рецепт',
                ]:
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
        elif request.command.lower() in ["измени рецепт",
                                  'исправь рецепт',
                                  'обнови рецепт',
                                  'обнови',
                                  'исправь',
                                  ]:
             user_storage["edit recipe"] = 1
             response.set_text("Скажите название рецепта, который хотите изменить")
             return response, user_storage
        elif user_storage["edit recipe"] > 0:
            response, user_storage = edit_recipe(request, response, user_storage, db)
            return  response, user_storage
        elif request.command.lower() in [
                "покажи рецепт",
                'воспроизведи рецепт',
                'открой рецепт',
                'открой',
                'покажи',
                ]:
             user_storage["get recipe"] = 1
             response.set_text("Скажите название рецепта, который хотите воспроизвести")
             return response, user_storage
         
        elif user_storage["get recipe"] > 0:
             response, user_storage = show_recipe(request, response, user_storage, db)
             return response, user_storage
         
        elif request.command.lower() == "помощь" or request.command.lower() == "что ты умеешь":
            response.set_text("""
                С моей помощью ты можешь сохранять свои рецепты, изменять их, удалять при необходимости
                Команды для работы со мной:
                    1) Добавь рецепт - открывает добавление рецепта
                    2) Измени рецепт - можно изменить название, добавить/удалить ингредиенты, добавить/удалить шаги рецепта
                    3) Покажи рецепт - можно получить ингредиенты и шаги
                    4) Выйти - для выхода из навыка
            """)
            return response, user_storage
        
        elif request.command.lower() == "пересчитай рецепт":
            user_storage["calculator"] = 1
            response.set_text("""Какой рецепт вы хотите пересчитать?""")
            return response, user_storage
        elif user_storage["calculator"] > 0:
            response, user_storage = calculat(request, response, user_storage, db)
            return response, user_storage
        
        elif request.command.lower() in [
                'список рецептов',
                'какие есть рецепты',
                'все рецепты',
                'покажи все мои рецепты',
                'покажи все рецепты',
                ]:
            response.set_text("""Какой рецепт вы хотите пересчитать?""")
            return response, user_storage
        else:
            response.set_text("Неизвестное действие, выберите то, что есть")
            response.set_buttons([
                    {'title':'Добавь рецепт', 'hide':True},
                    {'title':'Покажи рецепт', 'hide':True},
                    {'title':'Измени рецепт', 'hide':True},
                    {'title':'Пересчитай рецепт', 'hide':True},
                    {'title':'Удали рецепт', 'hide':True}])
            return response, user_storage
