#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from pymongo import MongoClient

def add_db(db, user_id, name, ingredients, steps):
    doc = {
        "user_id": user_id,
        "name": name.lower(),
        "ingredients" : ingredients,
        "steps" : steps
    }
    
    collection = db['recipes']
    collection.insert_one(doc)

def get_db(db, user_id, name):
    doc = db['recipes'].find_one({
            "user_id" : user_id,
            "name" : name.lower()
    })
    return doc

def delete_db(db, user_id, name):
    db["recipes"].delete_one({
            "user_id":user_id,
            "name":name
    })
        
def update_name_db(db, user_id, name_old, name_new):
    db["recipes"].update_one({"user_id":user_id, "name":name_old},
                              {"$set":{"name":name_new}})
    
def update_steps_db(db, user_id, name, steps):
    db["recipes"].update_one({"user_id":user_id, "name":name},
                              {"$set":{"steps":steps}})
    
def update_ingredients_db(db, user_id, name, ingredients):
    db["recipes"].update_one({"user_id":user_id, "name":name},
                              {"$set":{"ingredients":ingredients}})