#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from ossaca_model import *
from ossaca_database import *

class OssacaPluginType(IntEnum):
    GENERIC = 0
    PERSON = 1

class PluginState(IntEnum):
    UNLOADED = 0
    ATTACHED = 1
    LOADED = 2
    FAILED = 3

class OssacaPlugin:
    '''
    Class describing a plugin, that will add features to Ossaca. A plugin can
    be a way to link with other softwares, in particular to handle the Person
    database.

    A plugin must impement :
     - .load(),

     - .destroy(), which should perform any kind of de-init.

    Plugins must inherit this class
    '''

    def __init__(self, name = "", type = OssacaPluginType.GENERIC):
        self.name = name
        self.type = type
        self.storage = None
        self.state = PluginState.UNLOADED
        self._mandatory_methods = ["load", "destroy"]

    def __self_check(self):
        t = type(self)
        method_list = [func for func in dir(t) if callable(getattr(t, func)) and not func.startswith("__")]

        for m in self._mandatory_methods:
            if not m in method_list:
                raise NotImplementedError("Missing method %s" % m)
                return False

        return True

    def _attach(self, storage):
        if not self.__self_check():
            self.state = PluginState.FAILED
            return False

        self.state = PluginState.ATTACHED
        self.storage = storage
        return True

    def _register(self):

        if self.load():
            self.storage.register_plugin(self)
            self.state = PluginState.LOADED
            return True
        else:
            return False

    def set_config(self, key, value):
        if self.storage is None:
            return

        self.storage.set_plugin_config(self, key, value)

    def get_config(self, key):
        if self.storage is None:
            return

        return self.storage.get_plugin_config(self, key)

class OssacaPersonProviderPlugin(OssacaPlugin):
    '''
    Class describing a plugin in charge of providing read access to a Person's
    database.

    This plugin must give access to the following methods :
     - .get_all_persons()
     - .get_person_by_id(id)
    '''

    def __init__(self, name = ""):
        OssacaPlugin.__init__(self, name, OssacaPluginType.PERSON)
        self._mandatory_methods.extend(["get_all_persons", "get_person_by_id"])


