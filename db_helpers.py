#! /usr/bin/python3
# -*- coding:utf-8 -*-
from flask import Flask, request, g
from datetime import *
from ossaca_database import *

app = Flask(__name__)

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

def get_dogs():
    dogs = getdb().get_all_dogs()
    return dogs

def add_new_dog(form):
    db = getdb()
    dog = Dog()
    dog.name = form['name']
    dog.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    dog.arrival_date = date.fromisoformat(form['adate'])
    dog.gender = form['gender']
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
    dog.gender = form['gender']
    dog.breed = form['breed']
    dog.color = form['color']
    dog.implant = form['implant']
    dog.neutered = form['neutered'] if 'neutered' in form else 0
    dog.ok_cats = form['ok_cats'] if 'ok_cats' in form else 0
    dog.character = form['char']
    dog.history = form['history']
    db.update(dog)

def get_cats():
    cats = getdb().get_all_cats()
    return cats

def add_new_cat(form):
    db = getdb()
    cat = Cat()
    cat.name = form['name']
    cat.birth_date = date.fromisoformat(form['bdate']) if form['bdate'] is not '' else None
    cat.arrival_date = date.fromisoformat(form['adate'])
    cat.gender = form['gender']
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
    cat.gender = form['gender']
    cat.breed = form['breed']
    cat.color = form['color']
    cat.implant = form['implant']
    cat.neutered = form['neutered'] if 'neutered' in form else 0
    cat.has_fiv = form['fiv'] if 'fiv' in form else 0
    cat.has_felv = form['felv'] if 'felv' in form else 0
    cat.character = form['char']
    cat.history = form['history']
    db.update(cat)
