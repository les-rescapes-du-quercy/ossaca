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

    def test_add_state(self):
        s = SQLiteStorage()
        s.connect("test.db")

        state = State()
        state.label = "test"
        state.description = "pouet"
        s.add(state)

        cursor = s.con.cursor()
        cursor.execute("SELECT COUNT(*) FROM state")
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)

        cursor.execute("SELECT * FROM state")
        row = cursor.fetchone()

        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], "test")
        self.assertEqual(row[2], "pouet")

        s.add(state)
        cursor = s.con.cursor()
        cursor.execute("SELECT COUNT(*) FROM state")
        row = cursor.fetchone()

        self.assertEqual(row[0], 2)
        s.close()

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

############################## Update ##########################################

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
