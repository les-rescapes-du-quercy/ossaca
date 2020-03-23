#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Module for the OSSACA data model.
'''

import datetime
from datetime import date
from datetime import time
from enum import IntEnum

class Gender(IntEnum):
    '''
    IntEnum representing a gender
    '''
    UNKNOWN = 0
    FEMALE = 1
    MALE = 2

class Type:
    '''
    Generic class describing an eumerable entity with a label, a description and
    an id

    :param id: Id of the Type
    :type id: int

    :param label: Label of the state
    :type label: str

    :param description: Text describing the state
    :type description: str
    '''
    def __init__(self, id = -1, label = "", description = ""):
        self.id = id
        self.label = label
        self.description = description

class State(Type):
    '''
    Class describing an animal state
    '''
    def __init__(self, id = -1, label = "", description = ""):
        Type.__init__(self, id, label, description)

class Animal:
    '''
    Class representing a generic animal.

    :param id: Unique animal identifier
    :type id: int

    :param name: The animal's name
    :type name: str

    :param birth_date: The animal's Date of birth
    :type birth_date: datetime.date

    :param arrival_date: The animal's arrival date
    :type arrival_date: datetime.date

    :param arrival_sheet: The Sheet describing the animal's arrival
    :type arrival_sheet: Sheet

    :param latest_sheet: The latest Sheet attached to this animal
    :type latest_sheet: Sheet

    :param gender: The animal's Gender
    :type gender: Gender

    :param breed: The animal's breed
    :type breed: str

    :param character: Text describing the animal's character, behaviour
    and habits
    :type character: str

    :param color: Text describing the animal's color
    :type color: str

    :param pictures: A list of URIs to some animal's picture
    :type pictures: str

    :param sponsors: An array of sponsors for this animal
    :type sponsors: Person

    :param implant: Microchip implant number of the animal
    :type implant: str

    :param neutered: Indication wether or not the animal is neutered
    :type neutered: bool

    :param history: Text describing the history of the animal
    :type history: str

    :param caresheets: List of medical cares given to this animal
    :type caresheets: List of CareSheets

    :param food_habits: Indicates how the animal is used to being feed
    :type food_habits: FoodHabit
    '''
    def __init__(self, id = -1, name = "", birth_date = None, arrival_date = None,
                 arrival_sheet = None, latest_sheet = None,
                 gender = Gender.UNKNOWN, breed = "", character = "",
                 color = "", pictures = [], sponsors = [], implant = "",
                 neutered = False, history = "", caresheets = [], food_habits = None):
        self.id = id
        self.name = name
        self.birth_date = birth_date if birth_date is not None else date.today()
        self.arrival_date = arrival_date if arrival_date is not None else date.today()
        self.arrival_sheet = arrival_sheet
        self.latest_sheet = latest_sheet
        self.gender = gender
        self.breed = breed
        self.character = character
        self.color = color
        self.pictures = pictures
        self.sponsors = sponsors
        self.implant = implant
        self.neutered = neutered
        self.history = history
        self.caresheets = caresheets
        self.food_habits = food_habits

class Dog(Animal):
    '''
    Class describing a dog

    :param ok_cats: Indicated if this dog can live with cats
    :type ok_cats: bool
    '''
    def __init__(self, id = -1, name = "", birth_date = None, arrival_date = None,
                 arrival_sheet = None, latest_sheet = None,
                 gender = Gender.UNKNOWN, breed = "", character = "",
                 color = "", pictures = [], sponsors = [], implant = "",
                 neutered = False, history = "", caresheets = [], food_habits = None,
                 ok_cats = False):
        Animal.__init__(self, id, name, birth_date, arrival_date, arrival_sheet,
                        latest_sheet, gender, breed, character, color, pictures,
                        sponsors, implant, neutered, history, caresheets,
                        food_habits)
        self.ok_cats = ok_cats

class Cat(Animal):
    '''
    Class describing a cat

    :param has_fiv: Indicates if the cat has been diagnosed with the Feline
    Immunodeficiency Virus
    :type has_fiv: bool

    :param has felv: Indicates if the cat has been diagnosed with the Feline
    Leukimia Virus
    :type has_felv: bool
    '''
    def __init__(self, id = -1, name = "", birth_date = None, arrival_date = None,
                 arrival_sheet = None, latest_sheet = None,
                 gender = Gender.UNKNOWN, breed = "", character = "",
                 color = "", pictures = [], sponsors = [], implant = "",
                 neutered = False, history = "", caresheets = [], food_habits = None,
                 has_fiv = False, has_felv = False):
        Animal.__init__(self, id, name, birth_date, arrival_date, arrival_sheet,
                        latest_sheet, gender, breed, character, color, pictures,
                        sponsors, implant, neutered, history, caresheets,
                        food_habits)
        self.has_fiv = False
        self.has_felv = False

class Care:
    '''
    A Class representing a care that can be given to an animal

    :param id: A unique identifier for this Care
    :type id: int

    :param type: Care type
    :type type: str

    :param dose: Dosage, if this is a medicine
    :type dose: str

    :param way: How the care is administrated
    :type way: str

    :param medecine_name: Name of the medicine
    :type medecine_name: str

    :param description: Description of the medecine
    :type description: str
    '''
    def __init__(self, id = -1, type = "", dose = "", way = "",
                 medecine_name = "", description = ""):
        self.id = id
        self.type = type
        self.dose = dose
        self.way = way
        self.medecine_name = medecine_name
        self.description = description

class CareSheet:
    '''
    A Care Sheet describes a care given to a particular animal at a given date

    :param id: Unique id for the care sheet
    :type id: int

    :param animal: Animal to which the care was given to
    :type animal: Animal

    :param care: The care given to the animal
    :type care: Care

    :param date: Date at which the care was given
    :type date: datetime.date

    :param time: Time at which the care was given
    :type time: datetime.time

    :param frequency: frequency at which the care must be given
    :type frequency: str

    :param given_by: Person who gives the care to the animal
    :type given_by: Person

    :param prescription_number: Number of the prescription given by the vet
    :type prescription_number: str

    :param dosage: Dose admistrated to the animal
    :type dosage: str
    '''
    def __init__(self, id = -1, animal = None, care = None, date = None,
                 time = None, frequency = "", given_by = None,
                 prescription_number = "", dosage = ""):
        self.id = id
        self.animal = animal
        self.care = care
        self.date = date if date is not None else datetime.date.today()
        self.time = time if time is not None else datetime.time.fromisoformat("00:00:00")
        self.frequency = frequency
        self.given_by = given_by
        self.prescription_number = prescription_number
        self.dosage = dosage

class FoodHabit:
    '''
    Class describing a feeding habit for an animal, such as what type of food
    and what quantities

    :param id: Unique identifier for this food habit
    :type id: int

    :param food: the food type to give
    :type food: Food

    :param bowl: The way to give the food, in terms of quantities
    :type bowl: Bowl
    '''
    def __init__(self, id = -1, food = None, bowl = None):
        self.id = id
        self.food = food
        self.bowl = bowl

class Bowl(Type):
    '''
    Class representing a way to give food
    '''
    def __init__(self, id = -1, label = "", description = ""):
        Type.__init__(self, id, label, description)

class Food(Type):
    '''
    A food type to give to an animal
    '''
    def __init__(self, id = -1, label = "", description = ""):
        Type.__init__(self, id, label, description)

class LocationType(IntEnum):
    '''
    Describes the various types of locations for an animal
    '''

    BOX = 0
    VET = 1
    FOSTER_FAMILY = 2
    OTHER = 3

class Location:

    '''
    Describes the location of an animal. Depending on the location_type, the
    id points to the relevant location.

    :param id: Unique identifier for this location
    :type id: int

    :param location_type: The type of location the animal is at
    :type location_type: LocationType

    :param box: The Box where the animal is. Only relevant if location_type is
    BOX.
    :type box: Box

    :param person: The person that currently hosts the animal. Only relevant if
    location_type is VET or FOSTER_FAMILY.
    :type person: Person
    '''
    def __init__(self, id = -1, location_type = LocationType.OTHER, box = None,
                 person = None):
        self.id = id
        self.location_type = location_type
        self.box = box
        self.person = person

class Sheet:
    '''
    A Sheet describes a state or location change for the animal.

    :param id: An unique id for the Sheet
    :type id: int

    :param date: Time of the sheet edition
    :type date: datetime.date

    :param animal; The animal concerned by this sheet
    :type animal: Animal

    :param state: The new state of the animal
    :type state: State

    :param location: The location of the animal
    :type location: Location
    '''
    def __init__(self, id = -1, date = None, animal = None, state = None,
                 location = None):
        self.id = id
        self.date = date if date is not None else datetime.date.today()
        self.animal = animal
        self.state = state
        self.location = location

class Box:
    '''
    :param id: A unique identifier for this box
    :type id: int

    :param label: Box label
    :type label: str

    :param description: Text description of the box
    :type description: str

    :param surface_area: Surface area of the box, in squared meters
    :type surface_area: int
    '''
    def __init__(self, id = -1, label = "", description = "", surface_area = 0):
        self.id = id
        self.label = label
        self.description = description
        self.surface_area = surface_area


