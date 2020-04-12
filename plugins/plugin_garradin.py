#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ossaca_model import *
from ossaca_database import *
from ossaca_plugin import *

class GarradinPlugin(OssacaPersonProviderPlugin):
    '''
    Plugin to retrieve Person infos in a garradin database
    '''
    def __init__(self):
        OssacaPersonProviderPlugin.__init__(self, "test_person_plugin2")

    def load(self):
        return True

    def destroy(self):
        pass

    def get_person_by_id(self):
        return None

    def get_all_persons(self):
        return []

