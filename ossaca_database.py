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
                   species_id integer,
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
                   surface_area integer,
                   position text,
                   condition text,
                   particularity text
                   )''')

        con.commit()
        con.close()

    def connect(self, db_path):

        if not os.path.isfile(db_path):
            self.create(db_path)

        self.con = sqlite3.connect(db_path)
        self.con.row_factory = sqlite3.Row

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

    def __type_from_row(self, type_cls, row):
        return type_cls(
                    id = row['id'],
                    label = row['label'],
                    description = row['description']
               )

    def state_from_row(self, row):
        return self.__type_from_row(State, row)

    def bowl_from_row(self, row):
        return self.__type_from_row(Bowl, row)

    def food_from_row(self, row):
        return self.__type_from_row(Food, row)

    def __get_all(self, cls, get_from_row):
        table = SQLiteStorage.tables[cls]
        query = "SELECT * FROM " + table
        from_row = getattr(self, get_from_row)
        elems = []

        cursor = self.con.cursor()
        for row in cursor.execute(query):
            elems.append(from_row(row))

        return elems

    def __get_by_id(self, cls, get_from_row, id):
        table = SQLiteStorage.tables[cls]
        query = "SELECT * FROM " + table + " WHERE id = ?"
        from_row = getattr(self, get_from_row)

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        if row is None:
            return None

        return from_row(row)

    def get_all_states(self):
        return self.__get_all(State, "state_from_row")

    def get_state_by_id(self, id):
        return self.__get_by_id(State, "state_from_row", id)

    def get_all_foods(self):
        return self.__get_all(Food, "food_from_row")

    def get_food_by_id(self, id):
        return self.__get_by_id(Food, "food_from_row", id)

    def get_all_bowls(self):
        return self.__get_all(Bowl, "bowl_from_row")

    def get_bowl_by_id(self, id):
        return self.__get_by_id(Bowl, "bowl_from_row", id)

    @classmethod
    def params_animal(cls, animal):
        return {
                "species_id" : animal.species,
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

    def animal_from_row(self, row):
        return Animal(
            id = row['id'],
            species = row['species_id'],
            name = row['name'],
            birth_date = date.fromisoformat(row['birth_date']) if row['birth_date'] is not '' else None,
            arrival_date = date.fromisoformat(row['arrival_date']) if row['arrival_date'] is not '' else None,
            arrival_sheet = None,
            latest_sheet = None,
            gender = row['gender'],
            breed = row['breed'],
            character = row['character'],
            color = row['color'],
            pictures = row['pictures'].split(',') if row['pictures'] is not '' else [],
            implant = row['implant'],
            neutered = row['neutered'],
            history = row['history'],
            food_habits = self.get_foodhabit_by_id(row['food_habit_id']) if row['food_habit_id'] is not '' else None,
        )

    def get_all_animals_by_species(self, species):

        #Dogs and Cats have a specific treatment
        if species == Species.DOG:
            return self.get_all_dogs()

        if species == Species.CAT:
            return self.get_all_cats()

        query = "SELECT * FROM animal WHERE species_id = ?"
        animals = []

        cursor = self.con.cursor()

        for row in cursor.execute(query, [species]):
            animal = self.animal_from_row(row)
            self.__link_animal(animal)
            animals.append(animal)

        return animals

    def get_all_animals(self):
        animals = []
        for species in Species:
            animals.extend(self.get_all_animals_by_species(species))

        return animals

    def get_all_animals_by_box_id(self, id):
        animals = []
        query = '''
        SELECT animal.id FROM animal
        LEFT JOIN sheet ON animal.latest_sheet_id = sheet.id
        LEFT JOIN location ON sheet.location_id = location.id
        LEFT JOIN box ON location.box_id = box.id
        WHERE location.location_type = ? AND box.id = ?
        '''

        cursor = self.con.cursor()
        cursor.execute(query, [LocationType.BOX, id])

        rows = cursor.fetchall()

        for row in rows:
            animals.append(self.get_animal_by_id(row['id']))

        return animals

    def __get_animal_by_id_simple(self, id):
        # Try to get a dog
        animal = self.__get_dog_by_id_simple(id)
        if animal is not None:
            return animal

        # Try to get a cat
        animal = self.__get_cat_by_id_simple(id)
        if animal is not None:
            return animal

        # This is not a dog nor a cat, so build a generic animal
        query = "SELECT * FROM animal WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        if row is None:
            return None

        return self.animal_from_row(row)

    def __link_animal(self, animal):

        if animal is None:
            return None

        cursor = self.con.cursor()
        query = '''
                SELECT arrival_sheet_id, latest_sheet_id, food_habit_id
                FROM animal
                WHERE animal.id = ?
                '''

        cursor.execute(query, [animal.id])
        [arrival_sheet_id, latest_sheet_id, food_habit_id] = cursor.fetchone()

        if arrival_sheet_id is not None and arrival_sheet_id > 0:
            animal.arrival_sheet = self.__get_sheet_by_id_simple(arrival_sheet_id)
            animal.arrival_sheet.animal = animal

        if latest_sheet_id is not None and latest_sheet_id > 0:
            animal.latest_sheet = self.__get_sheet_by_id_simple(latest_sheet_id)
            animal.latest_sheet.animal = animal

    def get_animal_by_id(self, id):
        # Try to get a dog
        animal = self.get_dog_by_id(id)
        if animal is not None:
            return animal

        # Try to get a cat
        animal = self.get_cat_by_id(id)
        if animal is not None:
            return animal

        animal = self.__get_animal_by_id_simple(id)
        if animal is not None:
            self.__link_animal(animal)

        return animal

    @classmethod
    def params_dog(cls, dog):
        return {
                "ok_cats" : dog.ok_cats,
                "category" : dog.category
        }

    def dog_from_row(self, row):
        return Dog(
            id = row['id'],
            species = row['species_id'],
            name = row['name'],
            birth_date = date.fromisoformat(row['birth_date']) if row['birth_date'] is not '' else None,
            arrival_date = date.fromisoformat(row['arrival_date']) if row['arrival_date'] is not '' else None,
            arrival_sheet = None,
            latest_sheet = None,
            gender = row['gender'],
            breed = row['breed'],
            character = row['character'],
            color = row['color'],
            pictures = row['pictures'].split(',') if row['pictures'] is not '' else [],
            implant = row['implant'],
            neutered = row['neutered'],
            history = row['history'],
            food_habits = self.get_foodhabit_by_id(row['food_habit_id']) if row['food_habit_id'] is not '' else None,
            ok_cats = row['ok_cats'],
            category = row['category']
        )

    def get_all_dogs(self):
        query = ''' SELECT animal.*, dog.category, dog.ok_cats FROM dog
                    LEFT JOIN animal ON dog.animal_id = animal.id
                    '''
        dogs = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            dog = self.dog_from_row(row)
            self.__link_animal(dog)
            dogs.append(dog)

            # Todo : Build care list
        return dogs

    def __get_dog_by_id_simple(self, id):
        query = ''' SELECT animal.*, dog.category, dog.ok_cats FROM dog
                    LEFT JOIN animal ON dog.animal_id = animal.id
                    WHERE animal.id = ?'''

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        if row is None:
            return None

        return self.dog_from_row(row)

    def get_dog_by_id(self, id):
        dog = self.__get_dog_by_id_simple(id)

        if dog is not None:
            self.__link_animal(dog)

        return dog

    @classmethod
    def params_cat(cls, cat):
        return {
                "has_fiv" : cat.has_fiv,
                "has_felv" : cat.has_felv
        }

    def cat_from_row(self, row):
        return Cat(
            id = row['id'],
            species = row['species_id'],
            name = row['name'],
            birth_date = date.fromisoformat(row['birth_date']) if row['birth_date'] is not '' else None,
            arrival_date = date.fromisoformat(row['arrival_date']) if row['arrival_date'] is not '' else None,
            arrival_sheet = None,
            latest_sheet = None,
            gender = row['gender'],
            breed = row['breed'],
            character = row['character'],
            color = row['color'],
            pictures = row['pictures'].split(',') if row['pictures'] is not '' else [],
            implant = row['implant'],
            neutered = row['neutered'],
            history = row['history'],
            food_habits = self.get_foodhabit_by_id(row['food_habit_id']) if row['food_habit_id'] is not '' else None,
            has_fiv = row['has_fiv'],
            has_felv = row['has_felv']
        )

    def get_all_cats(self):
        query = ''' SELECT animal.*, cat.has_fiv, cat.has_felv FROM cat
                    LEFT JOIN animal ON cat.animal_id = animal.id
                '''
        cats = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            cat = self.cat_from_row(row)
            self.__link_animal(cat)
            cats.append(cat)

        return cats

    def __get_cat_by_id_simple(self, id):
        query = ''' SELECT animal.*, cat.has_fiv, cat.has_felv FROM cat
                    LEFT JOIN animal ON cat.animal_id = animal.id
                    WHERE animal.id = ?'''

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        if row is None:
            return None

        return self.cat_from_row(row)

    def get_cat_by_id(self, id):
        cat = self.__get_cat_by_id_simple(id)

        if cat is not None:
            self.__link_animal(cat)

        return cat

    def get_animals_by_box_id(self, box_id):
        return []

    @classmethod
    def params_care(cls, care):
        return {
            "type" : care.type,
            "dose" : care.dose,
            "way" : care.way,
            "medecine_name" : care.medecine_name,
            "description" : care.description
        }

    def care_from_row(self, row):
        return Care(
                id = row['id'],
                type = row['type'],
                dose = row['dose'],
                way = row['way'],
                medecine_name = row['medecine_name'],
                description = row['description']
        )

    def get_all_cares(self):
        return self.__get_all(Care, "care_from_row")

    def get_care_by_id(self, id):
        return self.__get_by_id(Care, "care_from_row", id)

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

    def caresheet_from_row(self, row):
        return CareSheet(
                    id = row['id'],
                    animal = self.get_animal_by_id(row['animal_id']) if row['animal_id'] > 0 else None,
                    care = self.get_care_by_id(row['care_id']) if row['care_id'] > 0 else None,
                    date = date.fromisoformat(row['date']) if row['date'] is not '' else None,
                    time = time.fromisoformat(row['time']) if row['time'] is not '' else None,
                    frequency = row['frequency'],
                    given_by = None, #TODO
                    prescription_number = row['prescription_number'],
                    dosage = row['dosage']
                )
    def get_all_caresheets(self):
        return self.__get_all(CareSheet, "caresheet_from_row")

    def get_caresheet_by_id(self, id):
        return self.__get_by_id(CareSheet, "caresheet_from_row", id)

    def get_all_caresheets_by_animal_id(self, animal_id):
        query = "SELECT * FROM caresheet WHERE animal_id = ?"
        caresheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query, [animal_id]):
            caresheets.append(self.caresheet_from_row(row))

        return caresheets

    @classmethod
    def params_foodhabit(cls, foodhabit):
        return {
            "food_id" : foodhabit.food.id if foodhabit.food is not None else -1,
            "bowl_id" : foodhabit.bowl.id if foodhabit.bowl is not None else -1,
        }

    def foodhabit_from_row(self, row):
        return FoodHabit(
                    id = row['id'],
                    food = self.get_food_by_id(row['food_id']) if row['food_id'] > 0 else None,
                    bowl = self.get_bowl_by_id(row['bowl_id']) if row['bowl_id'] > 0 else None,
                )

    def get_all_foodhabits(self):
        return self.__get_all(FoodHabit, "foodhabit_from_row")

    def get_foodhabit_by_id(self, id):
        return self.__get_by_id(FoodHabit, "foodhabit_from_row", id)

    @classmethod
    def params_location(cls, location):
        return {
            "location_type" : location.location_type,
            "box_id" : location.box.id if location.box is not None else -1,
            "person_id" : location.person.id if location.person is not None else -1
        }

    def location_from_row(self, row):
        return Location(
                    id = row['id'],
                    location_type = row['location_type'],
                    box = self.get_box_by_id(row['box_id']) if row['box_id'] > 0 else None,
                    person = None
                )

    def get_all_locations(self):
        return self.__get_all(Location, "location_from_row")

    def get_location_by_id(self, id):
        return self.__get_by_id(Location, "location_from_row", id)

    @classmethod
    def params_sheet(cls, sheet):
        return {
                "date" : sheet.date.isoformat() if sheet.date is not None else None,
                "animal_id" : sheet.animal.id if sheet.animal is not None else -1,
                "state_id" : sheet.state.id if sheet.state is not None else -1,
                "location_id" : sheet.location.id if sheet.location is not None else -1
        }

    def sheet_from_row(self, row):
        return Sheet(
                    id = row['id'],
                    date = date.fromisoformat(row['date']) if row['date'] is not '' else None,
                    animal = None,
                    state = self.get_state_by_id(row['state_id']) if row['state_id'] > 0 else None,
                    location = self.get_location_by_id(row['location_id']) if row['location_id'] > 0 else None,
                )

    def get_all_sheets(self):
        query = "SELECT * FROM sheet"
        sheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query):
            sheet = self.sheet_from_row(row)
            self.__link_sheet(sheet)
            sheets.append(sheet)

        return sheets

    def __link_sheet(self, sheet):
        query = "SELECT animal_id FROM sheet WHERE id = ?"

        cursor = self.con.cursor()
        cursor.execute(query, [sheet.id])
        [animal_id] = cursor.fetchone()

        animal = self.__get_animal_by_id_simple(animal_id)
        sheet.animal = animal

        if animal is not None:
            self.__link_animal(animal)

    def __get_sheet_by_id_simple(self, id):
        return self.__get_by_id(Sheet, "sheet_from_row", id)

    def get_sheet_by_id(self, id):
        sheet = self.__get_sheet_by_id_simple(id)

        if sheet is not None:
            self.__link_sheet(sheet)

        return sheet

    def get_all_sheets_by_animal_id(self, animal_id):
        query = "SELECT * FROM sheet where animal_id = ?"
        sheets = []

        cursor = self.con.cursor()

        for row in cursor.execute(query, [animal_id]):
            sheet = self.sheet_from_row(row)
            self.__link_sheet(sheet)
            sheets.append(sheet)

        return sheets

    @classmethod
    def params_box(cls, box):
        return {
                "label" : box.label,
                "description" : box.description,
                "surface_area" : box.surface_area,
                "position" : box.position,
                "condition" : box.condition,
                "particularity" : box.particularity
        }

    def box_from_row(self, row):
        return Box(
                    id = row['id'],
                    label = row['label'],
                    description = row['description'],
                    surface_area = row['surface_area'],
                    position = row['position'],
                    condition = row['condition'],
                    particularity = row['particularity'],
                )

    def get_all_boxes(self):
        return self.__get_all(Box, "box_from_row")

    def get_box_by_id(self, id):
        return self.__get_by_id(Box, "box_from_row", id)

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

    def update_animal_sheet(self, sheet):

        if sheet.animal is None:
            return

        if sheet.animal.id <= 0:
            return

        animal = self.get_animal_by_id(sheet.animal.id)

        if animal is None:
            return

        if animal.arrival_sheet is None:
            animal.arrival_sheet = sheet

        animal.latest_sheet = sheet

        self.update(animal)

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

        if isinstance(obj, Sheet):
            self.update_animal_sheet(obj)

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

