#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from db_api import *

def add_recipe(request, response, user_storage, db):
    if user_storage["add recipe"] == 1:
        ingr = request.command.lower().split()
        user_storage["ingredients"] = ingr
        #k = add_recipe(db, request.user_id, request.command)
        response.set_text("Хотите добавить еще ингредиенты? (да/нет)")
        user_storage["add recipe"] = 2
        return response, user_storage
    elif user_storage["add recipe"] == 2:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 1
            response.set_text = response.set_text("Назови ингредиенты в формате [название ингредиента] [количество] [мера]")
        elif request.command.lower() == "нет":
            user_storage["add recipe"] = 3
            response.set_text = response.set_text("Хотите назвать шаги приготовления?")
        return response, user_storage
    elif user_storage["add recipe"] == 3:
        if request.command.lower() == "да":
            user_storage["add recipe"] = 4
            response.set_text = response.set_text("Назови шаги в формате Шаг 1 [описание шага] Шаг 2 [описание шага]")
        elif request.command.lower() == "нет":
            user_storage = {"add recipe" : 0, "get recipe" : 0}
            #add_recipe(db, request.user_id, user_storage["name"], user_storage["ingredients"], user_storage["steps"])
            response.set_text = response.set_text("Спасибо, рецепт добавлен!")
        return response, user_storage
    elif user_storage["add recipe"] == 4:
        user_storage["steps"] += request.command.lower()
        response.set_text = response.set_text("Хотите назвать шаги приготовления?")
        user_storage["add recipe"] = 3
        return response, user_storage