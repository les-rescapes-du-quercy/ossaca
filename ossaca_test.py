#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import os
import os.path
from ossaca_model import *
from ossaca_database import *

########################### DB handling ########################################

class TestOssacaDB(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def test_create(self):
        s = SQLiteStorage()
        self.assertFalse(os.path.exists("test.db"))
        s.create("test.db")
        self.assertTrue(os.path.exists("test.db"))
        os.remove("test.db")

    def test_connect(self):
        s = SQLiteStorage()
        s.create("test.db")
        self.assertIsNone(s.con)
        s.connect("test.db")
        self.assertIsNotNone(s.con)
        s.close()
        os.remove("test.db")

    def test_connect_no_db(self):
        s = SQLiteStorage()
        self.assertFalse(os.path.exists("test.db"))
        self.assertIsNone(s.con)
        s.connect("test.db")
        self.assertIsNotNone(s.con)
        self.assertTrue(os.path.exists("test.db"))
        s.close()
        os.remove("test.db")

    def check_number_of_rows(self, table, n_rows):
        s = SQLiteStorage()
        s.connect("test.db")

        cursor = s.con.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + table)
        row = cursor.fetchone()

        self.assertEqual(row[0], n_rows)

        s.close()

    def __insert(self, obj):
        s = SQLiteStorage()
        s.connect("test.db")

        s.add(obj)
        s.close()

    def insertion_test(self, obj, table):

        self.__insert(obj)

        s = SQLiteStorage()
        s.connect("test.db")

        self.check_number_of_rows(table, 1)

        cursor = s.con.cursor()
        cursor.execute("SELECT * FROM " + table )
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)
        s.close()

    def check_table_row(self, table, id, values):
        s = SQLiteStorage()
        s.connect("test.db")

        cursor = s.con.cursor()
        cursor.execute("SELECT * FROM " + table + " WHERE id = ?", [id])
        row = cursor.fetchone()

        self.assertEqual(len(row), len(values))

        for read_value, expected_value in zip(row, values):
            self.assertEqual(read_value, expected_value)

        s.close()

    def insertion_and_check_test(self, table, obj, values):
        s = SQLiteStorage()
        s.connect("test.db")
        s.add(obj)
        s.close()

        self.check_table_row(table, 1, values)

    def test_add_empty_state(self):
        self.insertion_test(State(), "state")

    def test_add_default_state(self):
        self.insertion_and_check_test("state", State(), [1, "", ""])

    def test_add_state(self):
        self.insertion_and_check_test("state",
                            State(label = "Adopté",
                                  description = "L'animal est adopté"),
                            [1, "Adopté", "L'animal est adopté"])

    def test_add_empty_dog(self):
        self.insertion_test(Dog(), "dog")

    def test_add_default_dog(self):
        # default values
        self.insertion_and_check_test("animal", Dog(),
        [1, "", date.today().isoformat(), date.today().isoformat(), -1, -1, 0,
         "", "", "", "", "", 0, "", -1])

        self.check_table_row("dog", 1, [1, 1, 0, 0])

    def test_add_dog(self):
        # arbitrary values
        self.insertion_and_check_test("animal",
                Dog(
                name = "Louloute",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = None,
                latest_sheet = None,
                gender = Gender.FEMALE,
                breed = "Malinois croisé sharpei",
                character = "gentille avec du poil au nez",
                color = "verte",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = None,
                ok_cats = True,
                category = 1),
                [1, "Louloute", "2004-12-25", "2016-06-17", -1, -1, 1,
                 "Malinois croisé sharpei", "gentille avec du poil au nez",
                 "verte", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 -1])

        self.check_table_row("dog", 1, [1, 1, 1, 1])

    def test_add_dog_full(self):
        self.insertion_and_check_test("animal",
                Dog(
                name = "Louloute",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = Sheet(id = 2),
                latest_sheet = Sheet(id = 4),
                gender = Gender.FEMALE,
                breed = "Malinois croisé sharpei",
                character = "gentille avec du poil au nez",
                color = "verte",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = FoodHabit(id = 6),
                ok_cats = True,
                category = 2),
                [1, "Louloute", "2004-12-25", "2016-06-17", 2, 4, 1,
                 "Malinois croisé sharpei", "gentille avec du poil au nez",
                 "verte", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 6])

        self.check_table_row("dog", 1, [1, 1, 1, 2])

    def test_add_empty_cat(self):
        self.insertion_test(Cat(), "cat")

    def test_add_default_cat(self):
        # default values
        self.insertion_and_check_test("animal", Cat(),
        [1, "", date.today().isoformat(), date.today().isoformat(), -1, -1, 0,
         "", "", "", "", "", 0, "", -1])

        self.check_table_row("cat", 1, [1, 1, 0, 0])

    def test_add_cat(self):
        # arbitrary values
        self.insertion_and_check_test("animal",
                Cat(
                name = "Minette",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = None,
                latest_sheet = None,
                gender = Gender.FEMALE,
                breed = "Angora a poil ras",
                character = "gentille avec du poil au nez",
                color = "violette",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = None,
                has_fiv = True,
                has_felv = True),
                [1, "Minette", "2004-12-25", "2016-06-17", -1, -1, 1,
                 "Angora a poil ras", "gentille avec du poil au nez",
                 "violette", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 -1])

        self.check_table_row("cat", 1, [1, 1, 1, 1])

    def test_add_cat_full(self):
        self.insertion_and_check_test("animal",
                Cat(
                name = "Minette",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = Sheet(3),
                latest_sheet = Sheet(5),
                gender = Gender.FEMALE,
                breed = "Angora a poil ras",
                character = "gentille avec du poil au nez",
                color = "violette",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = FoodHabit(7),
                has_fiv = True,
                has_felv = False),
                [1, "Minette", "2004-12-25", "2016-06-17", 3, 5, 1,
                 "Angora a poil ras", "gentille avec du poil au nez",
                 "violette", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 7])

        self.check_table_row("cat", 1, [1, 1, 1, 0])

    def test_add_empty_care(self):
        self.insertion_test(Care(), "care")

    def test_add_default_care(self):
        self.insertion_and_check_test("care", Care(), [1, "", "", "", "", ""])

    def test_add_care(self):
        self.insertion_and_check_test("care",
                Care(type = "vaccin",
                     dose = "15mg",
                     way = "piqure",
                     medecine_name = "vaccinator",
                     description = "Vaccin contre le covid-19"),
                [1, "vaccin", "15mg", "piqure", "vaccinator",
                 "Vaccin contre le covid-19"])

    def test_add_empty_caresheet(self):
        self.insertion_test(CareSheet(), "caresheet")

    def test_add_default_caresheet(self):
        self.insertion_and_check_test("caresheet", CareSheet(),
                [1, -1, -1, date.today().isoformat(), "00:00:00",
                "", -1, "", ""])

    def test_add_caresheet(self):
        self.insertion_and_check_test("caresheet",
                    CareSheet(
                        animal = None,
                        care = None,
                        date = date.fromisoformat("2019-08-09"),
                        time = time.fromisoformat("12:04:34"),
                        frequency = "3 fois par jour",
                        given_by = None,
                        prescription_number = "P1234",
                        dosage = "2 gelules"),
                    [1, -1, -1, "2019-08-09", "12:04:34", "3 fois par jour",
                     -1, "P1234", "2 gelules"])

    def test_add_caresheet_full(self):
        self.insertion_and_check_test("caresheet",
                    CareSheet(
                        animal = Dog(id = 4),
                        care = Care(id = 7),
                        date = date.fromisoformat("2019-08-09"),
                        time = time.fromisoformat("12:04:34"),
                        frequency = "3 fois par jour",
                        given_by = None,
                        prescription_number = "P1234",
                        dosage = "2 gelules"),
                    [1, 4, 7, "2019-08-09", "12:04:34", "3 fois par jour",
                     -1, "P1234", "2 gelules"])

    def test_add_empty_foodhabit(self):
        self.insertion_test(FoodHabit(), "foodhabit")

    def test_add_default_foodhabit(self):
         self.insertion_and_check_test("foodhabit",
                FoodHabit(),
                [1, -1, -1])

    def test_add_foodhabit_full(self):
         self.insertion_and_check_test("foodhabit",
                FoodHabit(food = Food(id = 6), bowl = Bowl(id = 7)),
                [1, 6, 7])

    def test_add_empty_bowl(self):
        self.insertion_test(Bowl(), "bowl")

    def test_add_default_bowl(self):
        self.insertion_and_check_test("bowl",
                Bowl(),
                [1, "", ""])

    def test_add_bowl(self):
        self.insertion_and_check_test("bowl",
                Bowl(label = "Grosse gamelle",
                     description = "Une bonne grosse gamelle, miam miam"),
                [1, "Grosse gamelle", "Une bonne grosse gamelle, miam miam"])

    def test_add_empty_food(self):
        self.insertion_test(Food(), "food")

    def test_add_default_food(self):
        self.insertion_and_check_test("food",
                Food(),
                [1, "", ""])

    def test_add_food(self):
        self.insertion_and_check_test("food",
                Food(label = "Croquettes light",
                     description = "Croquettes allégées ou dietetiques"),
                [1, "Croquettes light", "Croquettes allégées ou dietetiques"])

    def test_add_empty_location(self):
        self.insertion_test(Location(), "location")

    def test_add_default_location(self):
        self.insertion_and_check_test("location",
                Location(),
                [1, LocationType.OTHER, -1, -1])

    def test_add_location(self):
        self.insertion_and_check_test("location",
                Location(location_type = LocationType.BOX, box = None, person = None),
                [1, LocationType.BOX, -1, -1])

    def test_add_location_full(self):
        self.insertion_and_check_test("location",
                Location(location_type = LocationType.BOX,
                         box = Box(id = 3),
                         person = None),
                [1, LocationType.BOX, 3, -1])

    def test_add_empty_sheet(self):
        self.insertion_test(Sheet(), "sheet")

    def test_add_default_sheet(self):
        self.insertion_and_check_test("sheet",
                Sheet(),
                [1, date.today().isoformat(), -1, -1, -1])

    def test_add_sheet(self):
        self.insertion_and_check_test("sheet",
                Sheet(date = date.fromisoformat("2017-11-11"),
                      animal = None, state = None, location = None),
                [1, "2017-11-11", -1, -1, -1])

    def test_add_sheet_full(self):
        cat = Cat()
        self.insertion_test(cat, "cat")

        self.assertEqual(cat.id, 1)
        self.assertIsNone(cat.arrival_sheet)
        self.assertIsNone(cat.latest_sheet)

        self.insertion_and_check_test("sheet",
                Sheet(date = date.fromisoformat("2017-11-11"),
                      animal = cat,
                      state = State(id = 2),
                      location = Location(id = 8)),
                [1, "2017-11-11", 1, 2, 8])

        self.check_table_row("animal", 1,
        [1, "", date.today().isoformat(), date.today().isoformat(), 1, 1, 0,
         "", "", "", "", "", 0, "", -1])

        self.__insert(Sheet(animal = cat))

        self.check_table_row("animal", 1,
        [1, "", date.today().isoformat(), date.today().isoformat(), 1, 2, 0,
         "", "", "", "", "", 0, "", -1])

    def test_add_empty_box(self):
        self.insertion_test(Box(), "box")

    def test_add_default_box(self):
        self.insertion_and_check_test("box", Box(), [1, "", "", 0])

    def test_add_box(self):
        self.insertion_and_check_test("box",
                Box(label = "Box 1", description = "Box 1 de l'allée centrale",
                    surface_area = 2),
                [1, "Box 1", "Box 1 de l'allée centrale", 2])

    def check_update(self, table, obj, new_obj, values):
        self.insertion_test(obj, table)

        s = SQLiteStorage()
        s.connect("test.db")

        s.update(new_obj)
        s.close()

        # Check that we still have one row after update
        self.check_number_of_rows(table, 1)

        # Check the new values
        self.check_table_row(table, new_obj.id, values)

    def test_update_state(self):
        self.check_update("state", State(),
                                   State(id = 1,
                                         label = "Adopté",
                                         description = "L'animal est adopté"),
                                   [1, "Adopté", "L'animal est adopté"]
        )

    def test_update_dog(self):
        self.check_update("animal", Dog(),
                Dog(
                id = 1,
                name = "Louloute",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = Sheet(id = 2),
                latest_sheet = Sheet(id = 4),
                gender = Gender.FEMALE,
                breed = "Malinois croisé sharpei",
                character = "gentille avec du poil au nez",
                color = "verte",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = FoodHabit(id = 6),
                ok_cats = True,
                category = 2),
                [1, "Louloute", "2004-12-25", "2016-06-17", 2, 4, 1,
                 "Malinois croisé sharpei", "gentille avec du poil au nez",
                 "verte", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 6]
        )

        self.check_table_row("dog", 1, [1, 1, 1, 2])

    def test_update_cat(self):
        self.check_update("animal", Cat(),
                Cat(
                id = 1,
                name = "Minette",
                birth_date = date.fromisoformat("2004-12-25"),
                arrival_date = date.fromisoformat("2016-06-17"),
                arrival_sheet = Sheet(3),
                latest_sheet = Sheet(5),
                gender = Gender.FEMALE,
                breed = "Angora a poil ras",
                character = "gentille avec du poil au nez",
                color = "violette",
                pictures = [],
                sponsors = [],
                implant = "1223446035OJCOJSDC",
                neutered = False,
                history = "Née au refuge",
                food_habits = FoodHabit(7),
                has_fiv = True,
                has_felv = False),
                [1, "Minette", "2004-12-25", "2016-06-17", 3, 5, 1,
                 "Angora a poil ras", "gentille avec du poil au nez",
                 "violette", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 7]
        )

        self.check_table_row("cat", 1, [1, 1, 1, 0])

    def test_update_care(self):
        self.check_update("care", Care(),
                Care(id = 1,
                     type = "vaccin",
                     dose = "15mg",
                     way = "piqure",
                     medecine_name = "vaccinator",
                     description = "Vaccin contre le covid-19"),
                [1, "vaccin", "15mg", "piqure", "vaccinator",
                 "Vaccin contre le covid-19"]
        )

    def test_update_caresheet(self):
        self.check_update("caresheet", CareSheet(),
                CareSheet(
                    id = 1,
                    animal = Dog(id = 4),
                    care = Care(id = 7),
                    date = date.fromisoformat("2019-08-09"),
                    time = time.fromisoformat("12:04:34"),
                    frequency = "3 fois par jour",
                    given_by = None,
                    prescription_number = "P1234",
                    dosage = "2 gelules"),
                [1, 4, 7, "2019-08-09", "12:04:34", "3 fois par jour",
                 -1, "P1234", "2 gelules"]
        )

    def test_update_foodhabit(self):
        self.check_update("foodhabit", FoodHabit(),
                FoodHabit(id = 1, food = Food(id = 6), bowl = Bowl(id = 7)),
                [1, 6, 7]
        )

    def test_update_bowl(self):
        self.check_update("bowl", Bowl(),
                Bowl(id = 1, label = "Grosse gamelle",
                     description = "Une bonne grosse gamelle, miam miam"),
                [1, "Grosse gamelle", "Une bonne grosse gamelle, miam miam"]
        )

    def test_update_food(self):
        self.check_update("food", Food(),
                Food(id = 1, label = "Croquettes light",
                     description = "Croquettes allégées ou dietetiques"),
                [1, "Croquettes light", "Croquettes allégées ou dietetiques"]
        )

    def test_update_location(self):
        self.check_update("location", Location(),
                Location(id = 1, location_type = LocationType.BOX,
                         box = Box(id = 3),
                         person = None),
                [1, LocationType.BOX, 3, -1]
        )

    def test_update_sheet(self):
        self.check_update("sheet", Sheet(),
                Sheet(id = 1,
                      date = date.fromisoformat("2017-11-11"),
                      animal = Cat(id = 9),
                      state = State(id = 2),
                      location = Location(id = 8)),
                [1, "2017-11-11", 9, 2, 8]
        )

    def test_update_box(self):
        self.check_update("box", Box(),
                Box(id = 1,
                    label = "Box 1", description = "Box 1 de l'allée centrale",
                    surface_area = 2),
                [1, "Box 1", "Box 1 de l'allée centrale", 2]
        )

############################## Delete ##########################################

    def check_delete(self, obj, table):
        self.insertion_test(obj, table)

        s = SQLiteStorage()
        s.connect("test.db")

        s.delete(obj)
        s.close()

        self.check_number_of_rows(table, 0)

    def test_delete_state(self):
        self.check_delete(State(id = 1), "state")

    def test_delete_dog(self):
        self.check_delete(Dog(id = 1), "dog")
        self.check_number_of_rows("animal", 0)

    def test_delete_cat(self):
        self.check_delete(Cat(id = 1), "cat")
        self.check_number_of_rows("animal", 0)

    def test_delete_care(self):
        self.check_delete(Care(id = 1), "care")

    def test_delete_caresheet(self):
        self.check_delete(CareSheet(id = 1), "caresheet")

    def test_delete_foodhabit(self):
        self.check_delete(FoodHabit(id = 1), "foodhabit")

    def test_delete_bowl(self):
        self.check_delete(Bowl(id = 1), "bowl")

    def test_delete_food(self):
        self.check_delete(Food(id = 1), "food")

    def test_delete_location(self):
        self.check_delete(Location(id = 1), "location")

    def test_delete_sheet(self):
        self.check_delete(Sheet(id = 1), "sheet")

    def test_delete_box(self):
        self.check_delete(Box(id = 1), "box")

############################### Read ###########################################

class TestOssacaDBAPI(unittest.TestCase):

    cares = []
    states = []
    foods = []
    bowls = []
    boxes = []
    locations = []
    foodhabits = []
    dogs = []
    cats = []
    sheets = []
    caresheets = []

    def populate_database(self, path):

        if os.path.exists(path):
            return

        s = SQLiteStorage()
        s.connect(path)

        TestOssacaDBAPI.cares = []

        # Build care list
        TestOssacaDBAPI.cares.append(
                    Care(type = "traitement", dose = "25mg", way = "orale",
                     medecine_name = "Clavubactin",
                     description = "Traitement des infections provoquées par les bactéries sensibles à l'amoxicilline en association avec l'acide clavulanique")
                    )

        TestOssacaDBAPI.cares.append(
                    Care(type = "traitement", dose = "50mg", way = "orale",
                     medecine_name = "Clavubactin", description = "Traitement des infections provoquées par les bactéries sensibles à l'amoxicilline en association avec l'acide clavulanique" )
                    )

        TestOssacaDBAPI.cares.append(
                    Care(type = "vaccin", dose = "10ml", way = "sous-cutanée",
                     medecine_name = "vaccinator",
                     description = "Vaccin contre le gros ventre" )
                    )

        TestOssacaDBAPI.cares.append(
                    Care(type = "operation", dose = "", way = "",
                     medecine_name = "",
                     description = "Operation de la molaire gauche" )
                    )

        TestOssacaDBAPI.cares.append(
                    Care(type = "checkup", dose = "", way = "",
                     medecine_name = "", description = "Checkup vétérinaire")
                    )

        TestOssacaDBAPI.cares.append(
                    Care(type = "traitement", dose = "", way = "Oreilles",
                     medecine_name = "",
                     description = "Nettoyage des oreilles avec compresse eet antiseptique" )
                    )
                    
        for care in TestOssacaDBAPI.cares:
            s.add(care)

        TestOssacaDBAPI.states = []

        # build state list
        TestOssacaDBAPI.states.append(
                        State(label = "Arrivé",
                        description = "L'ainmal est arrivé au refuge, en attente de voir son comportement")
                       )

        TestOssacaDBAPI.states.append(
                        State(label = "A l'essai",
                        description = "L'animal est placé en famille, pour essai de compatibilité en vue d'adoption")
                        )

        TestOssacaDBAPI.states.append(
                        State(label = "A l'adoption",
                        description = "L'animal est disponible à l'adoption")
                        )

        TestOssacaDBAPI.states.append(
                        State(label = "Quarantaine", description = "L'animal est placé en quarantaine")
                        )

        TestOssacaDBAPI.states.append(
                        State(label = "Vétérinaire", description = "L'animal est chez le vétérinaire")
                        )

        TestOssacaDBAPI.states.append(
                        State(label = "Adopté", description = "L'animal est adopté")
                        )

        for state in TestOssacaDBAPI.states:
            s.add(state)

        # build food list

        TestOssacaDBAPI.foods = []

        TestOssacaDBAPI.foods.append(
                        Food(label = "Croquettes chien adulte", description = "Croquettes pour chien adulte")
                        )

        TestOssacaDBAPI.foods.append(
                        Food(label = "Croquettes chat stérilisé", description = "Croquettes pour chat stérilisé")
                        )

        TestOssacaDBAPI.foods.append(
                        Food(label = "Croquettes chat gastro", description = "Croquettes gastro ou hypo pour chat")
                        )

        TestOssacaDBAPI.foods.append(
                        Food(label = "Paté chien bio sans boeuf", description = "Bonne patée bio miam miam")
                        )

        TestOssacaDBAPI.foods.append(
                        Food(label = "Paté chat", description = "Paté pour chat qui sent bon")
                        )

        TestOssacaDBAPI.foods.append(
                        Food(label = "Croquettes chiot", description = "Croquettes pour chiots")
                        )

        for food in TestOssacaDBAPI.states:
            s.add(food)

        # build bowl list
        TestOssacaDBAPI.bowls = []

        TestOssacaDBAPI.bowls.append(
                        Bowl(label = "petite gamelle", description = "une petite gamelle")
                        )

        TestOssacaDBAPI.bowls.append(
                        Bowl(label = "gamelle normale", description = "une gamelle de taille normale")
                        )

        TestOssacaDBAPI.bowls.append(
                        Bowl(label = "grosse gamelle", description = "une bonne grosse gamelle")
                        )

        TestOssacaDBAPI.bowls.append(
                        Bowl(label = "gamelle détrempée", description = "une gamelle normale bien ramolie")
                        )

        TestOssacaDBAPI.bowls.append(
                        Bowl(label = "a volonté", description = "Nourriture en accès libre à volonté")
                        )

        for bowl in TestOssacaDBAPI.bowls:
            s.add(bowl)

        # build box list
        TestOssacaDBAPI.boxes = []

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Box 1", description = "Box 1, allée 1, ensoleillé", surface_area = 3)
                        )

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Box 2", description = "Box 2, allée 1, ombragé", surface_area = 3)
                        )

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Box 3", description = "Box 3, allée 2, porte abimée", surface_area = 3)
                        )

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Box 4", description = "Box 4, allée 2, ensoleillé", surface_area = 4)
                        )

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Chatterie", description = "Chatterie", surface_area = 20)
                        )

        TestOssacaDBAPI.boxes.append(
                        Box(label = "Pouponnière", description = "La ou on met les chiots", surface_area = 5)
                        )

        for box in TestOssacaDBAPI.boxes:
            s.add(box)

        # Build location list
        TestOssacaDBAPI.locations = []

        TestOssacaDBAPI.locations.append(
                            Location(location_type = LocationType.BOX, box = TestOssacaDBAPI.boxes[0])
                            )

        TestOssacaDBAPI.locations.append(
                            Location(location_type = LocationType.BOX, box = TestOssacaDBAPI.boxes[1])
                            )

        TestOssacaDBAPI.locations.append(
                            Location(location_type = LocationType.BOX, box = TestOssacaDBAPI.boxes[4])
                            )

        TestOssacaDBAPI.locations.append(
                            Location(location_type = LocationType.FOSTER_FAMILY)
                            )

        TestOssacaDBAPI.locations.append(
                            Location(location_type = LocationType.VET)
                            )

        for location in TestOssacaDBAPI.locations:
            s.add(location)

        # Build food habits
        TestOssacaDBAPI.foodhabits = []

        self.foodhabits.append(FoodHabit(food = TestOssacaDBAPI.foods[0], bowl = TestOssacaDBAPI.bowls[2]))
        self.foodhabits.append(FoodHabit(food = TestOssacaDBAPI.foods[2], bowl = TestOssacaDBAPI.bowls[0]))
        self.foodhabits.append(FoodHabit(food = TestOssacaDBAPI.foods[3], bowl = TestOssacaDBAPI.bowls[1]))
        self.foodhabits.append(FoodHabit(food = TestOssacaDBAPI.foods[3], bowl = None))
        self.foodhabits.append(FoodHabit(food = TestOssacaDBAPI.foods[1], bowl = TestOssacaDBAPI.bowls[3]))
        self.foodhabits.append(FoodHabit(food = None, bowl = TestOssacaDBAPI.bowls[4]))

        for foodhabit in TestOssacaDBAPI.foodhabits:
            s.add(foodhabit)


        # Create Dogs
        TestOssacaDBAPI.dogs = []

        TestOssacaDBAPI.dogs.append(
                Dog(
                name = "Ichi",
                birth_date = date.fromisoformat("2019-04-21"),
                arrival_date = date.fromisoformat("2019-05-22"),
                gender = Gender.MALE,
                breed = "Malinois",
                character = "Gentil tout plein",
                color = "Brinje",
                pictures = ["http://loulou.com/picture.jpg", "http://prout.fr"],
                implant = "AZE123",
                neutered = True,
                history = "Maltraité dans une cage pendant l'enfance",
                food_habits = TestOssacaDBAPI.foodhabits[1],
                ok_cats = False,
                category = 0
                ))

        TestOssacaDBAPI.dogs.append(
                Dog(
                name = "Louloute",
                birth_date = date.fromisoformat("2017-12-12"),
                arrival_date = date.fromisoformat("2018-01-01"),
                gender = Gender.FEMALE,
                breed = "Staff x Caniche",
                character = "Super agressive avec tout le monde",
                color = "Blanc",
                pictures = ["/images/murder.jpg"],
                implant = "AIRO3991",
                neutered = True,
                history = "A tué ses parents",
                food_habits = TestOssacaDBAPI.foodhabits[3],
                ok_cats = False,
                category = 2
                ))

        TestOssacaDBAPI.dogs.append(
                Dog(
                name = "Pato",
                birth_date = date.fromisoformat("2015-04-04"),
                arrival_date = date.fromisoformat("2019-05-29"),
                gender = Gender.MALE,
                breed = "Griffon",
                character = "Gentil et mou",
                color = "Beige",
                pictures = [],
                neutered = False,
                history = "Abandonné dans un fossé",
                food_habits = None,
                ok_cats = True,
                category = 1
                ))

        TestOssacaDBAPI.dogs.append(
                Dog(
                name = "Roger",
                birth_date = date.fromisoformat("2010-02-14"),
                arrival_date = date.fromisoformat("2014-08-10"),
                gender = Gender.MALE,
                breed = "Chihuahua",
                character = "Mord les molets",
                color = "Marron",
                pictures = [],
                implant = "RORO009",
                neutered = True,
                history = "Propriétaire décédé",
                food_habits = TestOssacaDBAPI.foodhabits[4],
                ok_cats = True,
                category = 0
                ))

        for dog in TestOssacaDBAPI.dogs:
            s.add(dog)

        # Create Cats
        TestOssacaDBAPI.cats = []

        TestOssacaDBAPI.cats.append(
                Cat(
                name = "Happy",
                birth_date = date.fromisoformat("2011-11-11"),
                arrival_date = date.fromisoformat("2017-03-30"),
                gender = Gender.MALE,
                breed = "Chat européen",
                character = "Mange beaucoup",
                color = "Noir médaillon blanc",
                pictures = [],
                implant = "O182248",
                neutered = True,
                history = "Trouvé dans un abri de jardin",
                food_habits = TestOssacaDBAPI.foodhabits[5],
                has_fiv = False,
                has_felv = False
            ))

        TestOssacaDBAPI.cats.append(
                Cat(
                name = "Joy",
                birth_date = date.fromisoformat("2016-10-10"),
                arrival_date = date.fromisoformat("2018-08-10"),
                gender = Gender.FEMALE,
                breed = "Chat européen",
                character = "Miaule grave",
                color = "Gris tigré",
                pictures = [],
                implant = "JJ55",
                neutered = True,
                history = "Abandonnée",
                food_habits = TestOssacaDBAPI.foodhabits[0],
                has_fiv = False,
                has_felv = False
            ))

        TestOssacaDBAPI.cats.append(
                Cat(
                name = "Minou",
                birth_date = None,
                arrival_date = date.fromisoformat("2019-09-09"),
                gender = Gender.MALE,
                breed = "Angora",
                character = "Grumpy",
                color = "Blanc tigré roux",
                pictures = ["/cat/grumpy.jpg", "/cat/super_grimpy.jpg"],
                neutered = False,
                history = "A erré jusqu'au refuge. N'a qu'un oeil et 3 pattes",
                food_habits = TestOssacaDBAPI.foodhabits[2],
                has_fiv = True,
                has_felv = True
                ))

        for cat in TestOssacaDBAPI.cats:
            s.add(cat)

        # Create sheets
        TestOssacaDBAPI.sheets = []

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[0],
                      state = TestOssacaDBAPI.states[0],
                      location = TestOssacaDBAPI.locations[0]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[0],
                      state = TestOssacaDBAPI.states[1],
                      location = TestOssacaDBAPI.locations[1]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[0],
                      state = TestOssacaDBAPI.states[2],
                      location = TestOssacaDBAPI.locations[0]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[1],
                      state = TestOssacaDBAPI.states[0],
                      location = TestOssacaDBAPI.locations[2]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[2],
                      state = TestOssacaDBAPI.states[3],
                      location = TestOssacaDBAPI.locations[1]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.dogs[3],
                      state = TestOssacaDBAPI.states[1],
                      location = TestOssacaDBAPI.locations[3]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.cats[0],
                      state = TestOssacaDBAPI.states[4],
                      location = TestOssacaDBAPI.locations[4]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.cats[1],
                      state = TestOssacaDBAPI.states[1],
                      location = TestOssacaDBAPI.locations[4]))

        TestOssacaDBAPI.sheets.append(
                Sheet(animal = TestOssacaDBAPI.cats[2],
                      state = TestOssacaDBAPI.states[0],
                      location = TestOssacaDBAPI.locations[1]))

        for sheet in TestOssacaDBAPI.sheets:
            s.add(sheet)

        # Create caresheets
        TestOssacaDBAPI.caresheets = []

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[0],
                        care = TestOssacaDBAPI.cares[0],
                        date = date.fromisoformat("2020-02-01"),
                        time = time.fromisoformat("10:10:10"),
                        frequency = "1 fois par semaine",
                        prescription_number = "Doc_02.pdf",
                        dosage = "2 comprimés"
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[1],
                        care = TestOssacaDBAPI.cares[1],
                        date = date.fromisoformat("2020-02-02"),
                        time = time.fromisoformat("11:11:11"),
                        frequency = "2 fois par jour",
                        prescription_number = "ordonnance.pdf",
                        dosage = "3 cachetons"
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[1],
                        care = TestOssacaDBAPI.cares[3],
                        date = None,
                        time = None,
                        frequency = "oneshot",
                        prescription_number = "",
                        dosage = ""
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.cats[1],
                        care = TestOssacaDBAPI.cares[5],
                        date = date.fromisoformat("2020-02-02"),
                        time = time.fromisoformat("11:11:11"),
                        frequency = "5 fois par heures",
                        prescription_number = "prout.jpg",
                        dosage = "6 cachets"
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.cats[2],
                        care = TestOssacaDBAPI.cares[0],
                        date = date.fromisoformat("2020-02-02"),
                        time = time.fromisoformat("11:11:11"),
                        prescription_number = "3",
                        dosage = ""
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[3],
                        care = TestOssacaDBAPI.cares[0],
                        date = date.fromisoformat("2020-02-02"),
                        time = time.fromisoformat("11:11:18"),
                        frequency = "4 fois par mois",
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[3],
                        care = TestOssacaDBAPI.cares[4],
                        date = date.fromisoformat("2020-03-02"),
                        frequency = "2 fois par minute",
                        dosage = "4 piqures"
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[0],
                        care = TestOssacaDBAPI.cares[3],
                        date = date.fromisoformat("2020-04-02"),
                        time = time.fromisoformat("11:11:12"),
                        frequency = "one shot",
                        prescription_number = "1.jpg",
                ))

        TestOssacaDBAPI.caresheets.append(
                        CareSheet(
                        animal = TestOssacaDBAPI.dogs[3],
                        care = TestOssacaDBAPI.cares[4],
                        date = date.fromisoformat("2020-01-02"),
                        time = time.fromisoformat("11:11:12"),
                ))

        for caresheet in TestOssacaDBAPI.caresheets:
             s.add(caresheet)

    def compare_type(self, type_a, type_b):
        self.assertEqual(type_a.label, type_b.label)
        self.assertEqual(type_a.description, type_b.description)

    @classmethod
    def setUpClass(cls):
        if os.path.exists("example.db"):
            os.remove("example.db")

    def setUp(self):
        self.populate_database("example.db")

    def test_populate_database(self):

        if os.path.exists("example.db"):
            os.remove("example.db")

        self.populate_database("example.db")

        #os.remove("example.db")

    def test_get_all_states(self):
        s = SQLiteStorage()
        s.connect("example.db")

        states = s.get_all_states()
        self.assertEqual(len(states), len(self.states))

        for i in range(len(states)) :
            with self.subTest(i = i):
                self.compare_type(state[i], self.states[i])

        s.close()
        return

    def test_get_state_by_id(self):
        return

    def test_get_all_foods(self):
        return

    def test_get_food_by_id(self):
        return

    def test_get_all_bowls(self):
        return

    def test_get_bowl_by_id(self):
        return

    def test_get_all_animals(self):
        return

    def test_get_animal_by_id(self):
        return

    def test_get_all_dogs(self):
        return

    def test_get_dog_by_id(self):
        return

    def test_get_all_cats(self):
        return

    def test_get_cat_by_id(self):
        return

    def test_get_all_cares(self):
        return

    def test_get_care_by_id(self):
        return

    def test_get_all_caresheets(self):
        return

    def test_get_caresheet_by_id(self):
        return

    def test_get_all_caresheets_by_animal_id(self):
        return

    def test_get_all_foodhabits(self):
        return

    def test_get_foodhabit_by_id(self):
        return

    def test_get_all_locations(self):
        return

    def test_get_location_by_id(self):
        return

    def test_get_all_sheets(self):
        return

    def test_get_sheet_by_id(self):
        return

    def test_get_all_sheets_by_animal_id(self):
        return

    def test_get_all_boxes(self):
        return

    def test_get_box_by_id(self):
        return

if __name__ == '__main__':
    unittest.main()
