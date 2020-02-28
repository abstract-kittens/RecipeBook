#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pymongo import MongoClient

def add_recipe(db, user_id, name, ingredients, steps):
    doc = {
        "user_id": user_id,
        "name": name.lower(),
        "ingredients" : ingredients,
        "steps" : steps
    }
    
    collection = db['recipes']
    collection.insert_one(doc)

def get_recipe(db, user_id, name):
    doc = db['recipes'].find_one({
            "user_id" : user_id,
            "name" : name.lower()
    })
    return doc