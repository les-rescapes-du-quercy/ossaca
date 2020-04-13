#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ossaca_model import *
from ossaca_database import *
from ossaca_plugin import *

class GarradinPlugin(OssacaPersonProviderPlugin):
    '''
    Plugin to retrieve Person infos in a garradin database
    '''

    default_config = {
            "database_path" : "/var/www/garradin/association.sqlite"
    }

    def __init__(self):
        OssacaPersonProviderPlugin.__init__(self, "garradin_plugin")

    def __set_default_config(self):
        for key, val in GarradinPlugin.default_config.items():
            if self.get_config(key) is None:
                self.set_config(key, val)

    def load(self):
        self.__set_default_config()

        return True

    def destroy(self):
        pass

    def get_person_by_id(self):
        return None

    def get_all_persons(self):
        return []

