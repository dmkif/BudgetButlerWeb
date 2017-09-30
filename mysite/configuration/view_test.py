'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from configuration import views
from core import DBManager
from core.DatabaseModule import Database
import viewcore

class TesteSollzeit(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_init(self):
        self.set_up()
        views.handle_request(GetRequest())

    def teste_addKategorie(self):
        self.set_up()
        views.handle_request(PostRequest({'action':'add_kategorie', 'neue_kategorie':'test'}))
        assert viewcore.viewcore.database_instance().einzelbuchungen.get_alle_kategorien() == set(['test'])


if __name__ == '__main__':
    unittest.main()