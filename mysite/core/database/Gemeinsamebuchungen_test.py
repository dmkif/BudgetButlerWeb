'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date
import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')

from viewcore.converter import datum
import core.DatabaseModule as db
from core.database.Gemeinsamebuchungen import Gemeinsamebuchungen


class gemeinsame_buchungen(unittest.TestCase):

    def test_add_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        assert component_under_test.taint_number() == 0
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            'sebastian',
            1.23)
        assert component_under_test.taint_number() == 1

    def test_edit_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            'sebastian',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.edit(
            0,
            datum('2.1.2010'),
            'some other kategorie',
            'some other name',
            'sebastian',
            2.34)
        assert component_under_test.taint_number() == 1

    def test_delete_shouldTaint(self):
        component_under_test = Gemeinsamebuchungen()
        component_under_test.add(
            datum('1.1.2010'),
            'some kategorie',
            'some name',
            'sebastian',
            1.23)
        component_under_test.de_taint()
        assert component_under_test.taint_number() == 0
        component_under_test.delete(0)
        assert component_under_test.taint_number() == 1

