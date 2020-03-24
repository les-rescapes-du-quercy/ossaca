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

    def insertion_test(self, obj, table):
        s = SQLiteStorage()
        s.connect("test.db")

        s.add(obj)

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
        self.setUp()
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
                caresheets = [],
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
                caresheets = [],
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
                caresheets = [],
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
                caresheets = [],
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
        self.insertion_and_check_test("sheet",
                Sheet(date = date.fromisoformat("2017-11-11"),
                      animal = Cat(id = 9),
                      state = State(id = 2),
                      location = Location(id = 8)),
                [1, "2017-11-11", 9, 2, 8])

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
                caresheets = [],
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
                caresheets = [],
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
