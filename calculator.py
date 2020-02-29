#! /usr/bin/env python
# -*- coding: utf-8 -*-

import db_api

def calculat(request, response, user_storage, db):
    if request.command.lower() in [
            "отменить",
            'отмена',
            'назад'
            ]:
        response.set_text("Вы можете открыть другой рецепт")
        user_storage = {"add recipe" : 0, "get recipe" : 0,
                        "delete recipe" : 0, "edit recipe" : 0,
                        "calculator" : 0,
                        "name" : None, "ingredients":None,
                        "steps" : None}
        return response, user_storage
    
    elif user_storage["calculator"] == 1:
        user_storage["name"] = request.command.lower()
        if db_api.get_db(db, request.user_id, user_storage["name"]) == None:
            response.set_text("""Я не знаю этот рецепт""")
        else:
            response.set_text("""Как вы хотите пересчитать рецепт. 
                              Сделать его больше или меньше?""")
            user_storage["calculator"] = 2
        return response, user_storage
    
    elif user_storage["calculator"] == 2:
        if request.command.lower() == "больше":
            response.set_text("""На сколько процентов увеличить рецепт? Укажите только число""")
            user_storage["calculator"] = 3
            return response, user_storage
        
        elif request.command.lower() == "меньше":
            response.set_text("""На сколько процентов уменьшить рецепт? Укажите только число""")
            user_storage["calculator"] = 4
            return response, user_storage
        else: 
                response.set_text("Я вас не поняла")
                return response, user_storage
        
    elif user_storage["calculator"] == 3:
        if request.command.isnumeric() == True:
            s = ""
            db_rez = db_api.get_db(db, request.user_id, user_storage["name"])
            for i in db_rez["ingredients"]:
                num = int(i[1]) + (int(i[1]) * (int(request.command)/100))
                s += i[0] + " " + str(num) + " " + i[2] + "\n"

                
            response.set_text(s+ 'Посчитать еще?')
            user_storage["calculator"] = 5
            return response, user_storage
        else:
            response.set_text("""Я вас не поняла. Укажите процент на который нужно пересчитать блюдо""")
            return response, user_storage
        
    elif user_storage["calculator"] == 4:
        if request.command.isnumeric() == True:
            db_rez = db_api.get_db(db, request.user_id, user_storage["name"])
            
            s = ""
            for i in db_rez["ingredients"]:
                num = int(i[1]) * (int(request.command)/100)
                s += i[0] + " " + str(num) + " " + i[2] + "\n"
                
            response.set_text(s+ 'Посчитать еще?')
            user_storage["calculator"] = 5
            return response, user_storage
        else:
            response.set_text("""Я вас не поняла. Укажите процент на который нужно пересчитать блюдо""")
            return response, user_storage
    elif user_storage["calculator"] == 5:
        if request.command.lower() == "да":
            user_storage["calculator"] = 1
            response.set_text("Как вам пересчитать рецепт?")
            return response, user_storage
        elif request.command.lower() == "нет":
            response.set_text("Вы можете открыть другой рецепт")
            user_storage = {"add recipe" : 0, "get recipe" : 0,
                            "delete recipe" : 0, "edit recipe" : 0,
                            "calculator" : 0,
                            "name" : None, "ingredients":None,
                            "steps" : None}
            return response, user_storage
        else: 
            response.set_text("Я вас не поняла")
            return response, user_storage
    else: 
        response.set_text("Я вас не поняла")
        return response, user_storage     
            