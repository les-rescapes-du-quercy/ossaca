#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Module for the OSSACA data model.
'''

from datetime import date
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
    def __init__(self):
        Type.__init__(self)

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

    :param cares: List of medical cares given to this animal
    :type cares: List of Care

    :param food_habits: Indicates how the animal is used to being feed
    :type food_habits: FoodHabit
    '''
    def __init__(self, name = ""):
        self.id = -1
        self.name = name
        self.birth_date = date.today()
        self.arrival_date = date.today()
        self.arrival_sheet = None
        self.latest_sheet = None
        self.gender = Gender.UNKNOWN
        self.breed = ""
        self.character = ""
        self.color = ""
        self.pictures = ""
        self.sponsors = ""
        self.implant = ""
        self.neutered = False
        self.history = ""
        self.cares = []
        self.food_habits = None

class Dog(Animal):
    '''
    Class describing a dog

    :param ok_cats: Indicated if this dog can live with cats
    :type ok_cats: bool
    '''
    def __init__(self, name = ""):
        Animal.__init__(self, name)
        self.ok_cats = False

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
    def __init__(self):
        Animal.__init__(self, name)
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
    def __init__(self):
        self.id = -1
        self.type = ""
        self.dose = ""
        self.way = ""
        self.medecine_name = ""
        self.description = ""

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
    def __init__(self):
        self.id = -1
        self.animal = None
        self.care = None
        self.date = date.today()
        self.time = time.isoformat("00:00:00")
        self.frequency = ""
        self.given_by = None
        self.prescription_number = ""
        self.dosage = ""

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
    def __init__(self):
        self.id = -1
        self.food = None
        self.bowl = None

class Bowl(Type):
    '''
    Class representing a way to give food
    '''
    def __init__(self):
        Type.__init__(self)

class Food(Type):
    '''
    A food type to give to an animal
    '''
    def __init__(self):
        Type.__init__(self)

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
    def __init__(self):
        self.id = -1
        self.location_type = LocationType.OTHER
        self.box = None
        self.person = None

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
    def __init__(self):
        self.id = -1
        self.date = datetime.today()
        self.animal = None
        self.state = None
        self.location = None

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
    def __init__(self):
        self.id = -1
        self.label = ""
        self.description = ""
        self.surface_area = 0


