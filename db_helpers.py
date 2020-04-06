#! /usr/bin/python3
# -*- coding:utf-8 -*-
from flask import Flask, request, g
from datetime import *
from ossaca_database import *

app = Flask(__name__)

# ----------- GENERAL ----------- #

def getdb():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = SQLiteStorage()
        db.connect("ossaca_db.sqlite")
    return db

@app.teardown_appcontext
def closedb(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ----------- DOG ----------- #

def get_dogs():
    dogs = getdb().get_all_dogs()
    return dogs

def add_new_dog(form):
    db = getdb()
    dog = Dog()
    dog.name = form['name']
    dog.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    dog.arrival_date = date.fromisoformat(form['adate'])
    dog.gender = form['gender'] if 'gender' in form else Gender.UNKNOWN
    dog.breed = form['breed']
    dog.color = form['color']
    dog.implant = form['implant']
    dog.neutered = form['neutered'] if 'neutered' in form else 0
    dog.ok_cats = form['ok_cats'] if 'ok_cats' in form else 0
    dog.character = form['char']
    dog.history = form['history']
    db.add(dog)

def update_dog(form):
    db = getdb()
    dog = db.get_dog_by_id(form['id'])
    dog.name = form['name']
    dog.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    dog.arrival_date = date.fromisoformat(form['adate'])
    dog.gender = form['gender'] if 'gender' in form else Gender.UNKNOWN
    dog.breed = form['breed']
    dog.color = form['color']
    dog.implant = form['implant']
    dog.neutered = form['neutered'] if 'neutered' in form else 0
    dog.ok_cats = form['ok_cats'] if 'ok_cats' in form else 0
    dog.category = form['category']
    dog.character = form['char']
    dog.history = form['history']
    db.update(dog)

# ----------- CAT ----------- #

def get_cats():
    cats = getdb().get_all_cats()
    return cats

def add_new_cat(form):
    db = getdb()
    cat = Cat()
    cat.name = form['name']
    cat.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    cat.arrival_date = date.fromisoformat(form['adate'])
    cat.gender = form['gender'] if 'gender' in form else Gender.UNKNOWN
    cat.breed = form['breed']
    cat.color = form['color']
    cat.implant = form['implant']
    cat.neutered = form['neutered'] if 'neutered' in form else 0
    cat.has_fiv = form['fiv'] if 'fiv' in form else 0
    cat.has_felv = form['felv'] if 'felv' in form else 0
    cat.history = form['history']
    db.add(cat)

def update_cat(form):
    db = getdb()
    cat = db.get_cat_by_id(form['id'])
    cat.name = form['name']
    cat.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    cat.arrival_date = date.fromisoformat(form['adate'])
    cat.gender = form['gender'] if 'gender' in form else Gender.UNKNOWN
    cat.breed = form['breed']
    cat.color = form['color']
    cat.implant = form['implant']
    cat.neutered = form['neutered'] if 'neutered' in form else 0
    cat.has_fiv = form['fiv'] if 'fiv' in form else 0
    cat.has_felv = form['felv'] if 'felv' in form else 0
    cat.character = form['char']
    cat.history = form['history']
    db.update(cat)

# ----------- CARE ----------- #

def get_cares():
    cares = getdb().get_all_cares()
    return cares

def add_new_care(form):
    db = getdb()
    care = Care()
    care.type = form['type']
    care.way = form['way']
    care.dose = form['dose']
    care.medecine_name = form['name']
    care.description = form['desc']
    db.add(care)

def update_care(form):
    db = getdb()
    care = db.get_care_by_id(form['id_edit'])
    care.type = form['type']
    care.way = form['way']
    care.dose = form['dose']
    care.medecine_name = form['name']
    care.description = form['desc']
    db.update(care)

def del_care(id):
    db = getdb()
    care = db.get_care_by_id(id)
    db.delete(care)

# ----------- FOOD ----------- #

def get_bowls():
    bowls = getdb().get_all_bowls()
    return bowls

def add_new_bowl(form):
    db = getdb()
    bowl = Bowl()
    bowl.label = form['type']
    bowl.description = form['desc']
    db.add(bowl)

def update_bowl(form):
    db = getdb()
    bowl = db.get_bowl_by_id(form['id_edit_bowl'])
    bowl.label = form['type']
    bowl.description = form['desc']
    db.update(bowl)

def del_bowl(id):
    db = getdb()
    bowl = db.get_bowl_by_id(id)
    db.delete(bowl)

def get_foods():
    foods = getdb().get_all_foods()
    return foods

def add_new_food(form):
    db = getdb()
    food = Food()
    food.label = form['type']
    food.description = form['desc']
    db.add(food)

def update_food(form):
    db = getdb()
    food = db.get_food_by_id(form['id_edit_food'])
    food.label = form['type']
    food.description = form['desc']
    db.update(food)

def del_food(id):
    db = getdb()
    food = db.get_food_by_id(id)
    db.delete(food)
