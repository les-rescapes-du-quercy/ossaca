#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from ossaca_model import *
import os.path

class SQLiteStorage:
    '''
    Class used to store and load all entities described in the model using
    SQLite
    '''

    def __init__(self):
        self.tables = {
            State : "state",
            Dog : "dog",
            Cat : "cat",
            Care : "care",
            CareSheet : "caresheet",
            FoodHabit : "foodhabit",
            Bowl : "bowl",
            Food : "food",
            Location : "location",
            Sheet : "sheet",
            Box : "box"
        }

    def create(self, db_path):
        # doing so will create the database file.
        con = sqlite3.connect(db_path)

        c = con.cursor()

        # Create tables for all the model entities

        # Create Animal tables
        c.execute('''CREATE TABLE dog (
                   id integer NOT NULL PRIMARY KEY,
                   name text,
                   birth_date text,
                   arrival_date text,
                   arrival_sheet_id integer,
                   latest_sheet_id integer,
                   gender integer,
                   breed text,
                   character text,
                   color text,
                   pictures text,
                   implant text,
                   neutered integer,
                   history text,
                   food_habit_id integer,
                   ok_cats integer
                   )''')

        c.execute('''CREATE TABLE cat (
                   id integer NOT NULL PRIMARY KEY,
                   name text,
                   birth_date text,
                   arrival_date text,
                   arrival_sheet_id integer,
                   latest_sheet_id integer,
                   gender integer,
                   breed text,
                   character text,
                   color text,
                   pictures text,
                   implant text,
                   neutered integer,
                   history text,
                   food_habit_id integer,
                   has_fiv integer,
                   has_felv integer
                   )''')

        c.execute('''CREATE TABLE state(
                   id integer NOT NULL PRIMARY KEY,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE bowl(
                   id integer NOT NULL PRIMARY KEY,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE food(
                   id integer NOT NULL PRIMARY KEY,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE care(
                   id integer NOT NULL PRIMARY KEY,
                   type text,
                   dose text,
                   way text,
                   medecine_name text,
                   description text
                   )''')

        c.execute('''CREATE TABLE caresheet(
                   id integer NOT NULL PRIMARY KEY,
                   animal_id integer,
                   care_id integer,
                   date text,
                   time text,
                   frequency text,
                   given_by text,
                   prescription_number text,
                   dosage text
                   )''')

        c.execute('''CREATE TABLE foodhabit(
                   id integer NOT NULL PRIMARY KEY,
                   food_id integer,
                   bowl_id integer
                   )''')

        c.execute('''CREATE TABLE location(
                   id integer NOT NULL PRIMARY KEY,
                   location_type integer,
                   box_id integer,
                   person_id integer
                   )''')

        c.execute('''CREATE TABLE sheet(
                   id integer NOT NULL PRIMARY KEY,
                   date text,
                   animal_id integer,
                   state_id integer,
                   location_id integer
                   )''')

        c.execute('''CREATE TABLE box(
                   id integer NOT NULL PRIMARY KEY,
                   label text,
                   description text,
                   surface_area integer
                   )''')

        con.commit()
        con.close()

    def connect(self, db_path):

        if not os.path.isfile(db_path):
            print ("File", db_path, "doesn't exist, creating a new database")
            self.create(db_path)

        self.con = sqlite3.connect(db_path)

    def close(self):
        self.con.commit()
        self.con.close()

    @classmethod
    def params_type(cls, t):
        return {
                "label" : t.label,
                "description" : t.description
        }

    @classmethod
    def build_state(cls, fields):
        s = State()

        s.id = fields[0]
        s.label = fields[1]
        s.description = fields[2]

        return s

    @classmethod
    def build_bowl(cls, fields):
        b = Bowl()

        b.id = fields[0]
        b.label = fields[1]
        b.description = fields[2]

        return b

    @classmethod
    def build_food(cls, fields):
        f = Food()

        f.id = fields[0]
        f.label = fields[1]
        f.description = fields[2]

        return f

    @classmethod
    def params_dog(cls, dog):
        return {
                "name" : dog.name,
                "birth_date" : dog.birth_date.isoformat(),
                "arrival_date" : dog.arrival_date.isoformat(),
                "arrival_sheet_id" : dog.arrival_sheet.id if dog.arrival_sheet is not None else -1,
                "latest_sheet_id" : dog.latest_sheet.id if dog.latest_sheet is not None else -1,
                "gender" : dog.gender,
                "breed" : dog.breed,
                "character" : dog.character,
                "color" : dog.color, 
                "pictures" : ','.join(dog.pictures),
                "implant" : dog.implant,
                "neutered" : dog.neutered,
                "history" : dog.history,
                "food_habit_id" : dog.food_habit.id if dog.food_habits is not None else -1,
                "ok_cats" : dog.ok_cats
        }

    @classmethod
    def build_dog(cls, fields):
        d = Dog()

        d.id = fields[0]
        d.name = fields[1]
        d.arrival_date = date.fromisoformat(fields[2])
        d.arrival_sheet = None
        d.latest_sheet = None
        d.gender = fields[5]
        d.breed = fields[6]
        d.character = fields[7]
        d.color = fields[8]
        d.pictures = fields[9].split(',')
        d.implant = fields[10]
        d.neutered = fields[11]
        d.history = fields[12]
        d.food_habit = None
        d.ok_cats = fields[14]

        return d

    @classmethod
    def params_cat(cls, cat):
        return {
                "name" : cat.name,
                "birth_date" : cat.birth_date.isoformat(),
                "arrival_date" : cat.arrival_date.isoformat(),
                "arrival_sheet_id" : cat.arrival_sheet.id if cat.arrival_sheet is not None else -1,
                "latest_sheet_id" : cat.latest_sheet.id if cat.latest_sheet is not None else -1,
                "gender" : cat.gender,
                "breed" : cat.breed,
                "character" : cat.character,
                "color" : cat.color, 
                "pictures" : ','.join(cat.pictures),
                "implant" : cat.implant,
                "neutered" : cat.neutered,
                "history" : cat.history,
                "food_habit_id" : cat.food_habit.id if cat.food_habits is not None else -1,
                "ok_cats" : dog.ok_cats
        }

    @classmethod
    def build_dog(cls, fields):
        c = Cat()

        c.id = fields[0]
        c.name = fields[1]
        c.arrival_date = date.fromisoformat(fields[2])
        c.arrival_sheet = None
        c.latest_sheet = None
        c.gender = fields[5]
        c.breed = fields[6]
        c.character = fields[7]
        c.color = fields[8]
        c.pictures = fields[9].split(',')
        c.implant = fields[10]
        c.neutered = fields[11]
        c.history = fields[12]
        c.food_habit = None
        c.has_fiv = fields[14]
        c.has_felv = fields[15]

        return c

    @classmethod
    def parms_care(cls, care):
        return {
            "type" : care.type,
            "dose" : care.dose,
            "way" : care.way,
            "medecine_name" : care.medecine_name,
            "description" : care.description
        }

    @classmethod
    def build_care(cls, fields):
        c = Care()

        c.id = fields[0]
        c.type = fields[1]
        c.dose = fields[2]
        c.way = fields[3]
        c.medecine_name = fields[4]
        c.description = fields[5]

        return c

    @classmethod
    def params_caresheet(cls, caresheet):
        return {
                "animal_id" : caresheet.animal.id if caresheet.animal is not None else -1,
                "care_id" : caresheet.care.id if caresheet.care is not None else -1,
                "date" : caresheet.date.isoformat(),
                "time" : caresheet.time.isoformat(),
                "frequency" : caresheet.frequency,
                "given_by" : caresheet.given_by.id if caresheet.given_by is not None else -1,
                "prescription_number" : caresheet.prescription_number,
                "dosage" : caresheet.dosage
        }


    @classmethod
    def params_foodhabit(cls, foodhabit):
        return {
            "food_id" : foodhabit.food.id if foodhabit.food is not None else -1,
            "bowl_id" : foodhabit.bowl.id if foodhabit.bowl is not None else -1,
        }


    @classmethod
    def params_location(cls, location):
        return {
            "location_type" : location.location_type,
            "box_id" : location.box.id if location.box is not None else -1,
            "person_id" : location.person.id if location.person is not None else -1
        }

    @classmethod
    def params_sheet(cls, sheet):
        return {
                "date" : sheet.date.isoformat(),
                "animal_id" : sheet.animal.id if sheet.animal is not None else -1,
                "state_id" : sheet.state.id if sheet.state is not None else -1,
                "location_id" : sheet.location.id if sheet.location is not None else -1
        }

    @classmethod
    def params_box(cls, box):
        return {
                "label" : box.label,
                "description" : box.description,
                "surface_area" : box.surface_area
        }

    @classmethod
    def forge_query_insert(cls, table, params):
        placeholders = []
        values = []
        fields = []
        query = ""

        # To be sure that fields and values are in the same order. Might be
        # improved.
        for k,v in params.items():
            fields.append(k)
            values.append(v)
            placeholders.append("?")

        # The field validation and escaping will be done by the execute() method
        # from sqlite3
        query = " ".join([
                "INSERT INTO", table, 
                "(", ", ".join(fields), ")",
                "VALUES (", ', '.join(placeholders), ")"
                ])

        return [query, values]

    @classmethod
    def forge_query_update(cls, table, params, id):
        placeholders = []
        values = []
        fields = []
        query = ""

        # To be sure that fields and values are in the same order. Might be
        # improved.
        for k,v in params.items():
            fields.append(k + " = ?")
            values.append(v)

        values.append(id)

        # The field validation and escaping will be done by the execute() method
        # from sqlite3
        query = " ".join([
                "UPDATE", table,
                "SET", ", ".join(fields),
                "WHERE id = ?"
                ])

        return [query, values]

    @classmethod
    def get_query_params(cls, obj):

        if isinstance(obj, Type):
            params = SQLiteStorage.params_type(obj)
        if isinstance(obj, Dog):
            params = SQLiteStorage.params_dog(obj)
        elif isinstance(obj, Cat):
            params = SQLiteStorage.params_cat(obj)
        elif isinstance(obj, Care):
            params = SQLiteStorage.params_care(obj)
        elif isinstance(obj, CareSheet):
            params = SQLiteStorage.params_caresheet(obj)
        elif isinstance(obj, FoodHabit):
            params = SQLiteStorage.params_foodhabit(obj)
        elif isinstance(obj, Location):
            params = SQLiteStorage.params_location(obj)
        elif isinstance(obj, Sheet):
            params = SQLiteStorage.params_sheet(obj)
        elif isinstance(obj, Box):
            params = SQLiteStorage.params_box(obj)
        else:
            raise ValueError("Can get parameters for type %s" % type(obj).__name__)
            print("Unknown type", type(animal))
            params = {}

        return params

    def add(self, obj):
    
        params = SQLiteStorage.get_query_params(obj)
        table = self.tables[type(obj)]

        #build the query for the insertion
        [query, values] = SQLiteStorage.forge_query_insert(table, params)

        cursor = self.con.cursor()

        cursor.execute(query, values)

        self.con.commit()

    def update(self, obj):

        if obj.id < 1:
            raise ValueError("Can't update an object with id %d" % id)

        params = SQLiteStorage.get_query_params(obj)
        table = self.tables[type(obj)]

        #build the query for the insertion
        [query, values] = SQLiteStorage.forge_query_update(table, params, obj.id)

        cursor = self.con.cursor()

        cursor.execute(query, values)

        self.con.commit()

    def delete(self, obj):
        
        if obj.id < 1:
            raise ValueError("Can't delete an object with id %d", id)

        table = self.tables[type(obj)]
        query = "DELETE FROM " + table + " WHERE id = ?"
        params = [obj.id]

        cursor = self.con.cursor()
        cursor.execute(query, params)

        self.con.commit()

# Test code for ossaca_database
if __name__ == '__main__':

    s = SQLiteStorage()

    s.connect("ossaba_db.sqlite")

    ichi = Dog("Ichi")
    ichi.birth_date = date.fromisoformat('2019-02-14')
    ichi.gender = Gender.MALE
    
    s.add(ichi)
    ichi.name = "Ichie"
    ichi.gender = Gender.FEMALE
    s.add(ichi)

    ichi.id = 1

    ichi.name = "Gros Loulou"
    s.update(ichi)

    ichi.id = 2
    s.delete(ichi)

    s.close()

