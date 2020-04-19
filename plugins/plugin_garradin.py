#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ossaca_model import *
from ossaca_database import *
from ossaca_plugin import *
import unicodedata

class GarradinPlugin(OssacaPersonProviderPlugin):
    '''
    Plugin to retrieve Person infos in a garradin database
    '''

    default_config = {
            "database_path" : "/var/www/garradin/association.sqlite",
            "category_godmother" : "Marraine",
            "category_foster_family" : "FA",
            "category_volunteer" : "Bénévole",
            "category_adopter" : "Adoptant",
            "category_vet" : "Vétérinaire"
    }

    def __init__(self):
        OssacaPersonProviderPlugin.__init__(self, "garradin_plugin")
        self.cat_lookup = {}
        self.con = None

    def __set_default_config(self):
        for key, val in GarradinPlugin.default_config.items():
            if self.get_config(key) is None:
                self.set_config(key, val)

    def __normalize_str(self, input_str):
        '''
        To perform the category matching, we might want to include a bit of fuzzy
        matching, at least by dropping diacritics and being case insensitive.
        This method normalizes a string to perform the matching, by removing
        diacritics and converting to lowercase.

        This conversion method was found here :
        https://stackoverflow.com/a/517974
        '''
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c.lower() for c in nfkd_form if not unicodedata.combining(c)])

    def __load_category_lookup_table(self):
        self.cat_lookup[self.__normalize_str(self.get_config("category_godmother"))] = PersonType.GODMOTHER
        self.cat_lookup[self.__normalize_str(self.get_config("category_foster_family"))] = PersonType.FOSTER_FAMILY
        self.cat_lookup[self.__normalize_str(self.get_config("category_volunteer"))] = PersonType.VOLUNTEER
        self.cat_lookup[self.__normalize_str(self.get_config("category_adopter"))] = PersonType.ADOPTER
        self.cat_lookup[self.__normalize_str(self.get_config("category_vet"))] = PersonType.VET

    def __connect(self):
        path = self.get_config("database_path")
        if not os.path.isfile(path):
            os.stderr.write("Cannot find garradin database at %s" % path)
            return False

        self.con = sqlite3.connect(path)
        self.con.row_factory = sqlite3.Row

        return True

    def load(self):
        self.__set_default_config()
        self.__load_category_lookup_table()
        return self.__connect()

    def destroy(self):
        if self.con is not None:
            self.con.close()

    def __get_person_type_from_category(self, category):
        cat_norm = self.__normalize_str(category)
        if cat_norm in self.cat_lookup:
            return self.cat_lookup[cat_norm]
        else:
            return PersonType.OTHER

    def __person_from_row(self, row):
        return Person(
            id = row['id'],
            name = row['nom'],
            email = row['email'],
            address = Address(
                        street = row['adresse'],
                        postcode = row['code_postal'],
                        city = row['ville'],
                        country = row['pays']
                      ),
            phone = row['telephone'],
            type = self.__get_person_type_from_category(row['category'])
        )

    def get_person_by_id(self, id):
        query = '''
        SELECT membres.id, membres.nom, membres.email, membres.adresse,
               membres.code_postal, membres.ville, membres.pays, membres.telephone,
               membres_categories.nom as category
        FROM membres
        LEFT JOIN membres_categories ON membres.id_categorie = membres_categories.id
        WHERE membres.id = ?
        '''

        cursor = self.con.cursor()
        cursor.execute(query, [id])
        row = cursor.fetchone()

        if row is None:
            return None

        return self.__person_from_row(row)

    def get_all_persons(self):
        persons = []
        query = '''
        SELECT membres.id, membres.nom, membres.email, membres.adresse,
               membres.code_postal, membres.ville, membres.pays, membres.telephone,
               membres_categories.nom as category
        FROM membres
        LEFT JOIN membres_categories ON membres.id_categorie = membres_categories.id
        '''

        cursor = self.con.cursor()
        for row in cursor.execute(query) :
            persons.append(self.__person_from_row(row))

        return persons
