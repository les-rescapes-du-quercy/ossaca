#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sqlite3
from ossaca_model import *
import os.path
from enum import IntEnum

class SQLiteStorage:
    '''
    Class used to store and load all entities described in the model using
    SQLite
    '''

    tables = {
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

    def __init__(self):

        self.con = None

    def create(self, db_path):
        # doing so will create the database file.
        con = sqlite3.connect(db_path)

        c = con.cursor()

        # Create tables for all the model entities

        # Create Animal tables
        c.execute('''CREATE TABLE animal (
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
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
                   food_habit_id integer
                   )''')

        c.execute('''CREATE TABLE dog (
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   animal_id integer,
                   ok_cats integer,
                   category integer,
                   FOREIGN KEY(animal_id) REFERENCES animal(id)
                   )''')

        c.execute('''CREATE TABLE cat (
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   animal_id integer,
                   has_fiv integer,
                   has_felv integer,
                   FOREIGN KEY(animal_id) REFERENCES animal(id)
                   )''')

        c.execute('''CREATE TABLE state(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE bowl(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE food(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   label text,
                   description text
                   )''')

        c.execute('''CREATE TABLE care(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   type text,
                   dose text,
                   way text,
                   medecine_name text,
                   description text
                   )''')

        c.execute('''CREATE TABLE caresheet(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   animal_id integer,
                   care_id integer,
                   date text,
                   time text,
                   frequency text,
                   given_by integer,
                   prescription_number text,
                   dosage text
                   )''')

        c.execute('''CREATE TABLE foodhabit(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   food_id integer,
                   bowl_id integer
                   )''')

        c.execute('''CREATE TABLE location(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   location_type integer,
                   box_id integer,
                   person_id integer
                   )''')

        c.execute('''CREATE TABLE sheet(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   date text,
                   animal_id integer,
                   state_id integer,
                   location_id integer
                   )''')

        c.execute('''CREATE TABLE box(
                   id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                   label text,
                   description text,
                   surface_area integer
                   )''')

        con.commit()
        con.close()

    def connect(self, db_path):

        if not os.path.isfile(db_path):
            self.create(db_path)

        self.con = sqlite3.connect(db_path)

    def close(self):
        self.con.commit()
        self.con.close()

    def get_last_inserted_id(self, table):
            cursor = self.con.cursor()
            query = "SELECT seq FROM sqlite_sequence WHERE name = ?"
            cursor.execute(query, [table])
            row = cursor.fetchone()

            return row[0]

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

    def get_animal_by_id(self, id):
        return None

    @classmethod
    def params_animal(cls, animal):
        return {
                "name" : animal.name,
                "birth_date" : animal.birth_date.isoformat() if animal.birth_date is not None else "",
                "arrival_date" : animal.arrival_date.isoformat() if animal.arrival_date is not None else "",
                "arrival_sheet_id" : animal.arrival_sheet.id if animal.arrival_sheet is not None else -1,
                "latest_sheet_id" : animal.latest_sheet.id if animal.latest_sheet is not None else -1,
                "gender" : animal.gender,
                "breed" : animal.breed,
                "character" : animal.character,
                "color" : animal.color,
                "pictures" : ','.join(animal.pictures),
                "implant" : animal.implant,
                "neutered" : animal.neutered,
                "history" : animal.history,
                "food_habit_id" : animal.food_habits.id if animal.food_habits is not None else -1,
        }

    @classmethod
    def params_dog(cls, dog):
        return {
                "ok_cats" : dog.ok_cats,
                "category" : dog.category
        }

    def get_all_dogs(self):
        query = ''' SELECT * FROM dog
                    LEFT JOIN animal ON dog.animal_id = animal.id
                    '''
        dogs = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            dogs.append(
                    Dog(
                        ok_cats = row[2],
                        category = row[3],
                        id = row[4],
                        name = row[5],
                        birth_date = date.fromisoformat(row[6]) if row[6] is not '' else None,
                        arrival_date = date.fromisoformat(row[7]) if row[7] is not '' else None,
                        arrival_sheet = self.get_sheet_by_id(row[8]) if row[8] > 0 else None,
                        latest_sheet = self.get_sheet_by_id(row[9]) if row[9] > 0 else None,
                        gender = row[10],
                        breed = row[11],
                        character = row[12],
                        color = row[13],
                        pictures = row[14].split(','),
                        implant = row[15],
                        neutered = row[16],
                        history = row[17],
                        food_habits = self.get_foodhabit_by_id(row[18]) if row[18] > 0 else None,
                        caresheets = self.get_all_caresheets_by_animal_id(row[4])
                    )
            )

            # Todo : Build care list

        return dogs

    def get_dog_by_id(self, id):
        query = ''' SELECT * FROM dog
                    LEFT JOIN animal ON dog.animal_id = animal.id
                    WHERE animal.id = ?'''

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return  Dog(
                ok_cats = row[2],
                category = row[3],
                id = row[4],
                name = row[5],
                birth_date = date.fromisoformat(row[6]) if row[6] is not '' else None,
                arrival_date = date.fromisoformat(row[7]) if row[7] is not '' else None,
                arrival_sheet = self.get_sheet_by_id(row[8]) if row[8] > 0 else None,
                latest_sheet = self.get_sheet_by_id(row[9]) if row[9] > 0 else None,
                gender = row[10],
                breed = row[11],
                character = row[12],
                color = row[13],
                pictures = row[14].split(','),
                implant = row[15],
                neutered = row[16],
                history = row[17],
                food_habits = self.get_foodhabit_by_id(row[18]) if row[18] > 0 else None,
                caresheets = self.get_all_caresheets_by_animal_id(row[4])
         )

    @classmethod
    def params_cat(cls, cat):
        return {
                "has_fiv" : cat.has_fiv,
                "has_felv" : cat.has_felv
        }

    def get_all_cats(self):
        query = ''' SELECT * FROM cat
                    LEFT JOIN animal ON cat.animal_id = animal.id
                '''
        cats = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            cats.append(
                    Cat(
                        has_fiv = row[2],
                        has_felv = row[3],
                        id = row[4],
                        name = row[5],
                        birth_date = date.fromisoformat(row[6]) if row[6] is not '' else None,
                        arrival_date = date.fromisoformat(row[7]) if row[7] is not '' else None,
                        arrival_sheet = self.get_sheet_by_id(row[8]) if row[8] > 0 else None,
                        latest_sheet = self.get_sheet_by_id(row[9]) if row[9] > 0 else None,
                        gender = row[10],
                        breed = row[11],
                        character = row[12],
                        color = row[13],
                        pictures = row[14].split(','),
                        implant = row[15],
                        neutered = row[16],
                        history = row[17],
                        food_habits = self.get_foodhabit_by_id(row[18]) if row[18] > 0 else None,
                        caresheets = self.get_all_caresheets_by_animal_id(row[4])
                    )
            )

        return cats

    def get_cat_by_id(self, id):
        query = ''' SELECT * FROM cat
                    LEFT JOIN animal ON cat.animal_id = animal.id
                    WHERE animal.id = ?'''

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return  Cat(
                has_fiv = row[2],
                has_felv = row[3],
                id = row[4],
                name = row[5],
                birth_date = date.fromisoformat(row[6]) if row[6] is not '' else None,
                arrival_date = date.fromisoformat(row[7]) if row[7] is not '' else None,
                arrival_sheet = self.get_sheet_by_id(row[8]) if row[8] > 0 else None,
                latest_sheet = self.get_sheet_by_id(row[9]) if row[9] > 0 else None,
                gender = row[10],
                breed = row[11],
                character = row[12],
                color = row[13],
                pictures = row[14].split(','),
                implant = row[15],
                neutered = row[16],
                history = row[17],
                food_habits = self.get_foodhabit_by_id(row[18]) if row[18] > 0 else None,
                caresheets = self.get_all_caresheets_by_animal_id(row[4])
        )

    @classmethod
    def params_care(cls, care):
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
                        animal = self.get_animal_by_id(row[1]) if row[1] > 0 else None,
                        care = self.get_care_by_id(row[2]) if row[2] > 0 else None,
                        date = date.fromisoformat(row[3]) if row[3] is not '' else None,
                        time = time.fromisoformat(row[4]) if row[4] is not '' else None,
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
            animal = self.get_animal_by_id(row[1]) if row[1] > 0 else None,
            care = self.get_care_by_id(row[2]) if row[2] > 0 else None,
            date = date.fromisoformat(row[3]) if row[3] is not '' else None,
            time = time.fromisoformat(row[4]) if row[4] is not '' else None,
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
                        animal = self.get_animal_by_id(row[1]) if row[1] > 0 else None,
                        care = self.get_care_by_id(row[2]) if row[2] > 0 else None,
                        date = date.fromisoformat(row[3]) if row[3] is not '' else None,
                        time = time.fromisoformat(row[4]) if row[4] is not '' else None,
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
        query = "SELECT * FROM foodhabit"
        foodhabits = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            foodhabits.append(
                FoodHabit(
                    id = row[0],
                    food = self.get_food_by_id(row[1]) if row[1] > 0 else None,
                    bowl = self.get_else_by_id(row[2]) if row[2] > 0 else None,
                )
            )

        return foodhabit

    def get_foodhabit_by_id(self, id):
        query = "SELECT * FROM foodhabit WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return FoodHabit(
                    id = row[0],
                    food = self.get_food_by_id(row[1]) if row[1] > 0 else None,
                    bowl = self.get_else_by_id(row[2]) if row[2] > 0 else None,
        )

    @classmethod
    def params_location(cls, location):
        return {
            "location_type" : location.location_type,
            "box_id" : location.box.id if location.box is not None else -1,
            "person_id" : location.person.id if location.person is not None else -1
        }

    def get_all_locations(self):
        query = "SELECT * FROM location"
        locations = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            locations.append(
                Location(
                    id = row[0],
                    location_type = row[1],
                    box = self.get_box_by_id(row[2]) if row[2] > 0 else None,
                    person = None
                )
            )

        return locations

    def get_location_by_id(seld, id):
        query = "SELECT * FROM location WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return Location(
                    id = row[0],
                    location_type = row[1],
                    box = self.get_box_by_id(row[2]) if row[2] > 0 else None,
                    person = None
        )

    @classmethod
    def params_sheet(cls, sheet):
        return {
                "date" : sheet.date.isoformat() if sheet.date is not None else None,
                "animal_id" : sheet.animal.id if sheet.animal is not None else -1,
                "state_id" : sheet.state.id if sheet.state is not None else -1,
                "location_id" : sheet.location.id if sheet.location is not None else -1
        }

    def get_all_sheets(self):
        query = "SELECT * FROM sheet"
        sheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            sheets.append(
                Sheet(
                    id = row[0],
                    date = date.fromisoformat(row[1]) if row[1] is not '' else None,
                    animal = self.get_animal_by_id(row[2]) if row[2] > 0 else None,
                    state = self.get_state_by_id(row[3]) if row[3] > 0 else None,
                    location = self.get_location_by_id(row[4]) if row[4] > 0 else None,
                )
            )

        return sheets

    def get_sheet_by_id(self, id):
        query = "SELECT * FROM sheet WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return Sheet(
            id = row[0],
            date = date.fromisoformat(row[1]) if row[1] is not '' else None,
            animal = self.get_animal_by_id(row[2]) if row[2] > 0 else None,
            state = self.get_state_by_id(row[3]) if row[3] > 0 else None,
            location = self.get_location_by_id(row[4]) if row[4] > 0 else None,
        )

    def get_all_sheets_by_animal_id(self, animal_id):
        query = "SELECT * FROM sheet where animal_od = ?"
        sheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query, [animal_id]):
            sheets.append(
                Sheet(
                    id = row[0],
                    date = date.fromisoformat(row[1]) if row[1] is not '' else None,
                    animal = self.get_animal_by_id(row[2]) if row[2] > 0 else None,
                    state = self.get_state_by_id(row[3]) if row[3] > 0 else None,
                    location = self.get_location_by_id(row[4]) if row[4] > 0 else None,
                )
            )

        return sheets

    @classmethod
    def params_box(cls, box):
        return {
                "label" : box.label,
                "description" : box.description,
                "surface_area" : box.surface_area
        }

    def get_all_boxes(self):
        query = "SELECT * FROM box"
        boxes = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            boxes.append(
                Box(
                    id = row[0],
                    label = row[1],
                    description = row[2],
                    surface_area = row[3]
                )
            )

        return boxes

    def get_box_by_id(self, id):
        query = "SELECT * FROM box WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        return Box(
            id = row[0],
            label = row[1],
            description = row[2],
            surface_area = row[3]
        )

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

    def add_animal(self, animal):
        # First insert the generic animal info
        cursor = self.con.cursor()

        animal_params = SQLiteStorage.params_animal(animal)
        [query, values] = SQLiteStorage.forge_query_insert("animal", animal_params)

        cursor.execute(query, values)
        self.con.commit()

        table = SQLiteStorage.tables[type(animal)] if type(animal) in SQLiteStorage.tables else None

        # If we have some species-specific info, insert them
        if table is not None:
            animal_id = self.get_last_inserted_id("animal")

            species_params = SQLiteStorage.get_query_params(animal)
            species_params['animal_id'] = animal_id
            [query, values] = SQLiteStorage.forge_query_insert(table, species_params)

            cursor.execute(query, values)
            self.con.commit()

        animal.id = self.get_last_inserted_id("animal")

    def update_animal(self, animal):
        # First insert the generic animal info
        cursor = self.con.cursor()

        animal_params = SQLiteStorage.params_animal(animal)
        [query, values] = SQLiteStorage.forge_query_update("animal", animal_params, animal.id)

        cursor.execute(query, values)

        table = SQLiteStorage.tables[type(animal)] if type(animal) in SQLiteStorage.tables else None

        # If we have some species-specific info, insert them
        if table is not None:

            species_params = SQLiteStorage.get_query_params(animal)
            [query, values] = SQLiteStorage.forge_query_update_with_field(table,
                                species_params, animal.id, "animal_id")

            cursor.execute(query, values)

        self.con.commit()

    @classmethod
    def forge_query_update_with_field(cls, table, params, id, field):
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
                "WHERE " + field + " = ?"
                ])

        return [query, values]

    @classmethod
    def forge_query_update(cls, table, params, id):
        return SQLiteStorage.forge_query_update_with_field(table, params, id, "id")

    @classmethod
    def get_query_params(cls, obj):

        if isinstance(obj, Type):
            params = cls.params_type(obj)
        elif isinstance(obj, Dog):
            params = cls.params_dog(obj)
        elif isinstance(obj, Cat):
            params = cls.params_cat(obj)
        elif isinstance(obj, Care):
            params = cls.params_care(obj)
        elif isinstance(obj, CareSheet):
            params = cls.params_caresheet(obj)
        elif isinstance(obj, FoodHabit):
            params = cls.params_foodhabit(obj)
        elif isinstance(obj, Location):
            params = cls.params_location(obj)
        elif isinstance(obj, Sheet):
            params = cls.params_sheet(obj)
        elif isinstance(obj, Box):
            params = cls.params_box(obj)
        else:
            raise ValueError("Can get parameters for type %s" % type(obj).__name__)
            params = {}

        return params

    def add(self, obj):

        if isinstance(obj, Animal):
            self.add_animal(obj)
            return

        params = SQLiteStorage.get_query_params(obj)
        table = self.tables[type(obj)]

        #build the query for the insertion
        [query, values] = SQLiteStorage.forge_query_insert(table, params)

        cursor = self.con.cursor()

        cursor.execute(query, values)

        self.con.commit()

        obj.id = self.get_last_inserted_id(table)

    def update(self, obj):

        if obj.id < 1:
            raise ValueError("Can't update an object with id %d" % id)

        if isinstance(obj, Animal):
            self.update_animal(obj)
            return

        params = SQLiteStorage.get_query_params(obj)
        table = self.tables[type(obj)]

        #build the query for the insertion
        [query, values] = SQLiteStorage.forge_query_update(table, params, obj.id)

        cursor = self.con.cursor()

        cursor.execute(query, values)

        self.con.commit()

    def __delete_animal(self, animal):
        table = SQLiteStorage.tables[type(animal)] if type(animal) in SQLiteStorage.tables else None

        if table is not None:
            cursor = self.con.cursor()
            cursor.execute("SELECT id FROM " + table + " WHERE animal_id = ?", [animal.id])
            row = cursor.fetchone()

            cursor.execute("DELETE FROM " + table + " WHERE id = ?", [row[0]])

        cursor.execute("DELETE FROM animal WHERE id = ?", [animal.id])
        self.con.commit()

    def delete(self, obj):

        if obj.id < 1:
            raise ValueError("Can't delete an object with id %d", id)

        if isinstance(obj, Animal):
            self.__delete_animal(obj)
            return

        table = SQLiteStorage.tables[type(obj)]
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

    su_yeon = Cat(name = "Su Yeon")
    su_yeon.gender = Gender.FEMALE
    s.add(su_yeon)

    ichi.id = 1

    ichi.name = "Gros Loulou"
    ichi.ok_cats = True
    s.update(ichi)

    dogs = s.get_all_dogs()

    for dog in dogs:
        print (dog.name)

    cats = s.get_all_cats()

    for cat in cats:
        print (cat.name)

#    dog = s.get_dog_by_id(1)
#    print (dog.name)

    s.close()

