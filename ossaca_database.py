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

    def get_all_states(self):
        query = "SELECT * FROM state"
        states = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            states.append(State(row[0], row[1], row[2]))

        return states

    def get_state_by_id(self, id):
        query = "SELECT * FROM state WHERE id = ?"

        cursor = self.con.cursor()

        row = cursor.execute(query, [id])

        return State(row[0], row[1], row[2])

    def get_all_foods(self):
        query = "SELECT * FROM food"
        foods = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            foods.append(Food(row[0], row[1], row[2]))

        return foods

    def get_food_by_id(self, id):
        query = "SELECT * FROM food WHERE id = ?"

        cursor = self.con.cursor()

        row = cursor.execute(query, [id])

        return Food(row[0], row[1], row[2])

    def get_all_bowls(self):
        query = "SELECT * FROM bowl"
        bowls = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            bowls.append(Bowl(row[0], row[1], row[2]))

        return bowls

    def get_bowl_by_id(self, id):
        query = "SELECT * FROM bowl WHERE id = ?"

        cursor = self.con.cursor()

        row = cursor.execute(query, [id])

        return Bowl(row[0], row[1], row[2])

    # TODO
    def get_all_animals(self):
        return []

    # TODO FIXME
    def get_animal_by_id(self, id):
        return get_dog_by_id(self, id)

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

    def get_all_dogs(self):
        query = "SELECT * FROM dog"
        dogs = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            dogs.append(
                    Dog(
                        id = row[0],
                        name = row[1],
                        birth_date = date.fromisoformat(row[2]),
                        arrival_date = date.fromisoformat(row[3]),
                        arrival_sheet = get_sheet_by_id(self, row[4]) if row[4] > 0 else None,
                        latest_sheet = get_sheet_by_id(self, row[5]) if row[5] > 0 else None,
                        gender = row[6],
                        breed = row[7],
                        character = row[8],
                        color = row[9],
                        pictures = row[10].split(','),
                        implant = row[11],
                        neutered = row[12],
                        history = row[13],
                        food_habits = get_foodhabit_by_id(self, row[14]) if row[14] > 0 else None,
                        ok_cats = row[15],
                    )
            )

            # Todo : Build care list

        return dogs

    def get_dog_by_id(self, id):
        query = "SELECT * FROM dog WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return  Dog(
                id = row[0],
                name = row[1],
                birth_date = date.fromisoformat(row[2]),
                arrival_date = date.fromisoformat(row[3]),
                arrival_sheet = get_sheet_by_id(self, row[4]) if row[4] > 0 else None,
                latest_sheet = get_sheet_by_id(self, row[5]) if row[5] > 0 else None,
                gender = row[6],
                breed = row[7],
                character = row[8],
                color = row[9],
                pictures = row[10].split(','),
                implant = row[11],
                neutered = row[12],
                history = row[13],
                food_habits = get_foodhabit_by_id(self, row[14]) if row[14] > 0 else None,
                ok_cats = row[15]
         )

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

    def get_all_cats(self):
        query = "SELECT * FROM cat"
        cats = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            cats.append(
                    Cat(
                        id = row[0],
                        name = row[1],
                        birth_date = date.fromisoformat(row[2]),
                        arrival_date = date.fromisoformat(row[3]),
                        arrival_sheet = get_sheet_by_id(self, row[4]) if row[4] > 0 else None,
                        latest_sheet = get_sheet_by_id(self, row[5]) if row[5] > 0 else None,
                        gender = row[6],
                        breed = row[7],
                        character = row[8],
                        color = row[9],
                        pictures = row[10].split(','),
                        implant = row[11],
                        neutered = row[12],
                        history = row[13],
                        food_habits = get_foodhabit_by_id(self, row[14]) if raw[14] > 0 else None,
                        has_fiv = row[15],
                        has_felv = row[16]
                    )
            )

        return cats

    def get_cat_by_id(self, id):
        query = "SELECT * FROM cat WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return  Cat(
                id = row[0],
                name = row[1],
                birth_date = date.fromisoformat(row[2]),
                arrival_date = date.fromisoformat(row[3]),
                arrival_sheet = get_sheet_by_id(self, row[4]) if row[4] > 0 else None,
                latest_sheet = get_sheet_by_id(self, row[5]) if row[5] > 0 else None,
                gender = row[6],
                breed = row[7],
                character = row[8],
                color = row[9],
                pictures = row[10].split(','),
                implant = row[11],
                neutered = row[12],
                history = row[13],
                food_habits = get_foodhabit_by_id(self, row[14]) if raw[14] > 0 else None,
                has_fiv = row[15],
                has_felv = row[16]
         )

    @classmethod
    def parms_care(cls, care):
        return {
            "type" : care.type,
            "dose" : care.dose,
            "way" : care.way,
            "medecine_name" : care.medecine_name,
            "description" : care.description
        }

    def get_all_cares(self):
        query = "SELECT * FROM care"
        cares = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            care.append(
                    Care(
                        id = row[0],
                        type = row[1],
                        dose = row[2],
                        way = row[3],
                        medecine_name = row[4],
                        description = row[5]
                    )
            )

        return cares

    def get_care_by_id(self, id):
        query = "SELECT * FROM care WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return Care(
            id = row[0],
            type = row[1],
            dose = row[2],
            way = row[3],
            medecine_name = row[4],
            description = row[5]
        )

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

    def get_all_caresheets(self):
        query = "SELECT * FROM caresheet"
        caresheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            caresheets.append(
                    CareSheet(
                        id = row[0],
                        animal = get_animal_by_id(self, row[1]) if row[1] > 0 else None,
                        care = get_care_by_id(self, row[2]) if row[2] > 0 else None,
                        date = date.fromisoformat(row[3]),
                        time = time.fromisoformat(row[4]),
                        frequency = row[5],
                        given_by = None, #TODO
                        prescription_number = row[7],
                        dosage = row[8]
                    )
            )

        return caresheets

    def get_caresheet_by_id(self, id):
        query = "SELECT * FROM caresheet WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return CareSheet(
            id = row[0],
            animal = get_animal_by_id(self, row[1]) if row[1] > 0 else None,
            care = get_care_by_id(self, row[2]) if row[2] > 0 else None,
            date = date.fromisoformat(row[3]),
            time = time.fromisoformat(row[4]),
            frequency = row[5],
            given_by = None, #TODO
            prescription_number = row[7],
            dosage = row[8]
        )

    def get_all_caresheets_by_animal_id(self, animal_id):
        query = "SELECT * FROM caresheet WHERE animal_id = ?"
        caresheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query, [animal_id]):
            caresheets.append(
                    CareSheet(
                        id = row[0],
                        animal = get_animal_by_id(self, row[1]) if row[1] > 0 else None,
                        care = get_care_by_id(self, row[2]) if row[2] > 0 else None,
                        date = date.fromisoformat(row[3]),
                        time = time.fromisoformat(row[4]),
                        frequency = row[5],
                        given_by = None, #TODO
                        prescription_number = row[7],
                        dosage = row[8]
                    )
            )

        return caresheets

    @classmethod
    def params_foodhabit(cls, foodhabit):
        return {
            "food_id" : foodhabit.food.id if foodhabit.food is not None else -1,
            "bowl_id" : foodhabit.bowl.id if foodhabit.bowl is not None else -1,
        }

    def get_all_foodhabits(self):
        query = "SELECT * FROM foodhabits"
        caresheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            caresheets.append(
                    CareSheet(
                        id = row[0],
                        animal = get_animal_by_id(self, row[1]) if row[1] > 0 else None,
                        care = get_care_by_id(self, row[2]) if row[2] > 0 else None,
                        date = date.fromisoformat(row[3]),
                        time = time.fromisoformat(row[4]),
                        frequency = row[5],
                        given_by = None, #TODO
                        prescription_number = row[7],
                        dosage = row[8]
                    )
            )

        return caresheets

        return []

    def get_foodhabit_by_id(self, id):
        return None

    @classmethod
    def params_location(cls, location):
        return {
            "location_type" : location.location_type,
            "box_id" : location.box.id if location.box is not None else -1,
            "person_id" : location.person.id if location.person is not None else -1
        }

    def get_all_locations(self):
        return []

    def get_location_by_id(seld, id):
        return None

    @classmethod
    def params_sheet(cls, sheet):
        return {
                "date" : sheet.date.isoformat(),
                "animal_id" : sheet.animal.id if sheet.animal is not None else -1,
                "state_id" : sheet.state.id if sheet.state is not None else -1,
                "location_id" : sheet.location.id if sheet.location is not None else -1
        }

    def get_all_sheets(self):
        return []

    def get_sheet_by_id(self, id):
        return None

    def get_all_sheets_by_animal_id(self, animal_id):
        return []

    @classmethod
    def params_box(cls, box):
        return {
                "label" : box.label,
                "description" : box.description,
                "surface_area" : box.surface_area
        }

    def get_all_boxes(self):
        return []

    def get_box_by_id(self, id):
        return None

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

    s.connect("ossaca_db.sqlite")

    ichi = Dog(name = "Ichi")
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

    dogs = s.get_all_dogs()

    for dog in dogs:
        print (dog.name)

    dog = s.get_dog_by_id(1)
    print (dog.name)

    s.close()

