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

############################### Add ############################################

class TestDBAdd(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def insertion_test(self, obj, table):
        s = SQLiteStorage()
        s.connect("test.db")

        s.add(obj)

        cursor = s.con.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + table)
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)

        cursor.execute("SELECT * FROM " + table )
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)
        s.close()

    def insertion_and_check_test(self, table, obj, values):

        self.setUp()
        s = SQLiteStorage()
        s.connect("test.db")

        s.add(obj)

        cursor = s.con.cursor()
        cursor.execute("SELECT * FROM " + table )
        row = cursor.fetchone()

        self.assertEqual(len(row), len(values))

        for read_value, expected_value in zip(row, values):
            self.assertEqual(read_value, expected_value)

        s.close()

    def test_add_state(self):
        self.insertion_test(State(), "state")

    def test_add_empty_dog(self):
        self.insertion_test(Dog(), "dog")

    def test_add_default_dog(self):
        # default values
        self.insertion_and_check_test("dog", Dog(),
        [1, "", date.today().isoformat(), date.today().isoformat(), -1, -1, 0,
         "", "", "", "", "", 0, "", -1, 0])

    def test_add_dog(self):
        # arbitrary values
        self.insertion_and_check_test("dog",
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
                caresheets = [],
                food_habits = None,
                ok_cats = True),
                [1, "Louloute", "2004-12-25", "2016-06-17", -1, -1, 1,
                 "Malinois croisé sharpei", "gentille avec du poil au nez",
                 "verte", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 -1, 1])

    def test_add_empty_cat(self):
        self.insertion_test(Cat(), "cat")

    def test_add_default_cat(self):
        # default values
        self.insertion_and_check_test("cat", Cat(),
        [1, "", date.today().isoformat(), date.today().isoformat(), -1, -1, 0,
         "", "", "", "", "", 0, "", -1, 0, 0])

    def test_add_cat(self):
        # arbitrary values
        self.insertion_and_check_test("cat",
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
                caresheets = [],
                food_habits = None,
                has_fiv = True,
                has_felv = True),
                [1, "Minette", "2004-12-25", "2016-06-17", -1, -1, 1,
                 "Angora a poil ras", "gentille avec du poil au nez",
                 "violette", "", "1223446035OJCOJSDC", 0, "Née au refuge",
                 -1, 1, 1])

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

    def test_add_empty_foodhabit(self):
        self.insertion_test(FoodHabit(), "foodhabit")

    def test_add_default_foodhabit(self):
         self.insertion_and_check_test("foodhabit",
                FoodHabit(),
                [1, -1, -1])

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

    def test_add_empty_sheet(self):
        self.insertion_test(Sheet(), "sheet")

    def test_add_default_sheet(self):
        self.insertion_test(Sheet(), "sheet")

    def test_add_sheet(self):
        self.insertion_test(Sheet(), "sheet")

    def test_add_empty_box(self):
        self.insertion_test(Box(), "box")

    def test_add_default_box(self):
        self.insertion_test(Box(), "box")

    def test_add_box(self):
        self.insertion_test(Box(), "box")

    def test_location_full(self):
        return

    def test_foodhabit_full(self):
        return

    def test_sheet_full(self):
        return

    def test_care_full(self):
        return

    def test_dog_full(self):
        return

    def test_cat_full(self):
        return

############################## Update ##########################################

class TestDBUpdate(unittest.TestCase):

    def setUp(self):
        if os.path.exists("test.db"):
            os.remove("test.db")

    def insertion_test(self, obj, table):
        s = SQLiteStorage()
        s.connect("test.db")

        s.add(obj)

        cursor = s.con.cursor()
        cursor.execute("SELECT COUNT(*) FROM " + table)
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)

        cursor.execute("SELECT * FROM " + table )
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)
        s.close()

    def test_add_state(self):
        self.insertion_test(State(), "state")

    def test_add_dog(self):
        self.insertion_test(Dog(), "dog")

    def test_add_cat(self):
        self.insertion_test(Cat(), "cat")

    def test_add_care(self):
        self.insertion_test(Care(), "care")

    def test_add_caresheet(self):
        self.insertion_test(CareSheet(), "caresheet")

    def test_add_foodhabit(self):
        self.insertion_test(FoodHabit(), "foodhabit")

    def test_add_bowl(self):
        self.insertion_test(Bowl(), "bowl")

    def test_add_food(self):
        self.insertion_test(Food(), "food")

    def test_add_location(self):
        self.insertion_test(Location(), "location")

    def test_add_sheet(self):
        self.insertion_test(Sheet(), "sheet")

    def test_add_box(self):
        self.insertion_test(Box(), "box")


#State
#Dog
#Cat
#Care
#CareSheet
#FoodHabit
#Bowl
#Food
#Location
#Sheet
#Box

############################## Delete ##########################################

#State
#Dog
#Cat
#Care
#CareSheet
#FoodHabit
#Bowl
#Food
#Location
#Sheet
#Box

############################### Read ###########################################

#get_all_states()
#get_state_by_id(id)
#get_all_foods()
#get_food_by_id(id)
#get_all_bowls()
#get_bowl_by_id(id)
#get_all_animals()
#get_animal_by_id(id)
#get_all_dogs()
#get_dog_by_id(id)
#get_all_cats()
#get_cat_by_id(id)
#get_all_cares()
#get_care_by_id(id)
#get_all_caresheets()
#get_caresheet_by_id(id)
#get_all_caresheets_by_animal_id(animal_id)
#get_all_foodhabits()
#get_foodhabit_by_id(id)
#get_all_locations()
#get_location_by_id(seldid)
#get_all_sheets()
#get_sheet_by_id(id)
#get_all_sheets_by_animal_id(animal_id)
#get_all_boxes()
#get_box_by_id(id)


if __name__ == '__main__':
    unittest.main()
