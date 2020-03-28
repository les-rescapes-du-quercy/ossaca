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
