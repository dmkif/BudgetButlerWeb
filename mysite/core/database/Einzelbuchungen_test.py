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

import core.DatabaseModule as db
from core.database.Einzelbuchungen import Einzelbuchungen
from viewcore.converter import datum


class einzelbuchungen(unittest.TestCase):

    def test_getJahresausgaben_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahresausgaben_withNonMatchingDate_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/1990'), 'some kategorie', 'some name', -1.54)
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahresausgaben_withNonMatchingValue_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2016'), 'some kategorie', 'some name', 1.54)
        assert component_under_test.get_jahresausgaben(2016) == 0

    def test_getJahreseinnahmen_withEmptyDatabase_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.get_jahreseinnahmen(2016) == 0

    def test_getJahreseinnahmen_withNonMatchingDate_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/1990'), 'some kategorie', 'some name', -1.54)

    def test_getJahreseinnahmen_withNonMatchingValue_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2016'), 'some kategorie', 'some name', -1.54)
        assert component_under_test.get_jahreseinnahmen(2016) == 0

    def test_add(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Name[0] == 'some name'
        assert component_under_test.content.Kategorie[0] == 'some kategorie'
        assert component_under_test.content.Wert[0] == 1.54
        assert component_under_test.content.Tags[0] == []

    def test_aendere_beiEinzigerEinzelbuchung(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'some kategorie', 'some name', 1.54)
        component_under_test.edit(0, date.today(), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.content) == 1
        assert component_under_test.content.Datum[0] == date.today()
        assert component_under_test.content.Name[0] == 'some other name'
        assert component_under_test.content.Kategorie[0] == 'some other kategorie'
        assert component_under_test.content.Wert[0] == 2.65


    def test_aendere_beiVollerDatenbank(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2017'), '3kategorie', '3name', 1.54)
        component_under_test.add(datum('02/01/2017'), '2kategorie', '2name', 1.54)
        component_under_test.add(datum('03/01/2017'), '1kategorie', '1name', 1.54)

        assert component_under_test.content.Datum[0] == datum('01/01/2017')

        component_under_test.edit(0, datum('15/01/2017'), 'some other kategorie', 'some other name', 2.65)

        assert len(component_under_test.content) == 3
        assert set(component_under_test.content.Name) == set(['1name', '2name', 'some other name'])
        assert set(component_under_test.content.Datum) == set([datum('02/01/2017'), datum('03/01/2017'), datum('15/01/2017')])

        changed_row = component_under_test.content[component_under_test.content.Datum == datum('15/01/2017')]
        changed_row.reset_index(drop=True, inplace=True)
        assert changed_row.Name[0] == 'some other name'
        assert changed_row.Kategorie[0] == 'some other kategorie'
        assert changed_row.Wert[0] == 2.65

    def test_get_single_einzelbuchung(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '1kategorie', '1name', 1.54)

        result = component_under_test.get(0)

        assert result['index'] == 0
        assert result['Datum'] == date.today()
        assert result['Name'] == '1name'
        assert result['Kategorie'] == '1kategorie'
        assert result['Wert'] == 1.54

    def test_get_gesamtausgaben_nach_kategorie_withEmptyDatabase_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.get_gesamtausgaben_nach_kategorie() == {}

    def test_get_gesamtausgaben_nach_kategorie_shouldReturnResult(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '1kategorie', '1name', -1)
        component_under_test.add(date.today(), '1kategorie', '1name', -4)
        component_under_test.add(date.today(), '2kategorie', '1name', -3)

        result = component_under_test.get_gesamtausgaben_nach_kategorie()
        assert result.keys() == set(['1kategorie', '2kategorie'])
        assert result['1kategorie'] == -5
        assert result['2kategorie'] == -3

    def test_get_gesamtausgaben_nach_kategorie_withEinnahmen_shouldFilterEinnahmen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '1kategorie', '1name', 1)

        assert component_under_test.get_gesamtausgaben_nach_kategorie() == {}

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2012'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2013'), '1kategorie', '1name', 1)

        assert component_under_test.get_all().Datum[0].year == 2011
        assert component_under_test.get_all().Datum[1].year == 2012
        assert component_under_test.get_all().Datum[2].year == 2013

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '3kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '2kategorie', '1name', 1)

        assert component_under_test.get_all().Kategorie[0] == '1kategorie'
        assert component_under_test.get_all().Kategorie[1] == '2kategorie'
        assert component_under_test.get_all().Kategorie[2] == '3kategorie'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '3name', 1)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '2name', 1)

        assert component_under_test.get_all().Name[0] == '1name'
        assert component_under_test.get_all().Name[1] == '2name'
        assert component_under_test.get_all().Name[2] == '3name'

    def test_get_einzelbuchungen_shouldReturnListSortedBy_Datum_Kategorie_Name_Wert(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 10)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 5)

        assert component_under_test.get_all().Wert[0] == 1
        assert component_under_test.get_all().Wert[1] == 5
        assert component_under_test.get_all().Wert[2] == 10


    def test_edit_einzelbuchung_shouldRefreshSortingOfEinzelbuchungen(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2012'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2011'), '1kategorie', '1name', 1)
        component_under_test.add(datum('01/01/2013'), '1kategorie', '1name', 1)

        component_under_test.edit(0, datum('01/01/2020'), '1kategorie', '1name', 1)

        assert component_under_test.get_all().Datum[0].year == 2012
        assert component_under_test.get_all().Datum[1].year == 2013
        assert component_under_test.get_all().Datum[2].year == 2020

    def test_anzahl_withEmptyDB_shouldReturnZero(self):
        component_under_test = Einzelbuchungen()

        assert component_under_test.anzahl() == 0

    def test_anzahl_withOneEntry_shouldReturnOne(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2012'), '1kategorie', '1name', 1)

        assert component_under_test.anzahl() == 1


class gesamtausgaben_jahr(unittest.TestCase):

    def test_get_gesamtausgaben_jahr_withOneAusgabe_shouldReturnAusgabe(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'Some Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(date.today().year)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withOneAusgabeAndOneEinnahme_shouldReturnOnlyAusgabe(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), 'Some Kategorie', 'bla', -1)
        component_under_test.add(date.today(), 'Some Kategorie', 'bla', 11)

        result = component_under_test.get_gesamtausgaben_jahr(date.today().year)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withOneAusgabeAndOneAusgabeWithWrongYear_shouldReturnOnlyAusgabeOfMatchingYear(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add(datum('01/01/2014'), 'Some Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert result.index == ['Some Kategorie']
        print(result)
        assert result.Wert[0] == -1

    def test_get_gesamtausgaben_jahr_withTwoDifferentCategories_shouldReturnBothCategories(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add(datum('01/01/2017'), 'Some other Kategorie', 'bla', -1)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert set(result.index) == set(['Some Kategorie', 'Some other Kategorie'])

    def test_get_gesamtausgaben_jahr_withTwoDifferentDates_shouldReturnCummulatedResult(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2017'), 'Some Kategorie', 'bla', -1)
        component_under_test.add(datum('01/01/2017'), 'Some Kategorie', 'bla', -3)

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert result.index == ['Some Kategorie']
        assert result.Wert[0] == -4

    def test_get_gesamtausgaben_jahr_withEmptyDB_shouldReturnEmptyDataframe(self):
        component_under_test = Einzelbuchungen()

        result = component_under_test.get_gesamtausgaben_jahr(2017)

        assert set(result.index) == set()

    def test_get_jahresausgaben_nach_monat_withEmptyDB_shouldReturnEmptyDataframe(self):
        component_under_test = Einzelbuchungen()

        result = component_under_test.get_jahresausgaben_nach_monat(2017)

        assert set(result.index) == set()

    def test_getGesamtausgabenNachKategorieProzentual_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert result == {}

    def test_getGesamtausgabenNachKategorieProzentual_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', 10)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert result == {}

    def test_getGesamtausgabenNachKategorieProzentual_withOneEntry_shouldReturnKategorieWith100Percent(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert set(result.keys()) == set(['kategorie 1'])
        assert  result['kategorie 1'] == 100.00

    def test_getGesamtausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', -7.5)
        component_under_test.add(datum('01/01/2015'), 'kategorie 2', 'some name', -2.5)

        result = component_under_test.get_gesamtausgaben_nach_kategorie_prozentual()

        assert set(result.keys()) == set(['kategorie 1', 'kategorie 2'])
        assert  result['kategorie 1'] == 75.00
        assert  result['kategorie 2'] == 25.00

    def test_getJahresausgabenNachKategorieProzentual_withEmptyDB_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withEinnahme_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', 10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}


    def test_getJahresausgabenNachKategorieProzentual_withAusgabeAußerhalbDesJahres_shouldReturnEmptyDict(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2014'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert result == {}

    def test_getJahresausgabenNachKategorieProzentual_withOneEntry_shouldReturnKategorieWith100Percent(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', -10)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1'])
        assert  result['kategorie 1'] == 100.00

    def test_getJahresausgabenNachKategorieProzentual_withTwoEntrys_shouldReturnResult(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(datum('01/01/2015'), 'kategorie 1', 'some name', -7.5)
        component_under_test.add(datum('01/01/2015'), 'kategorie 2', 'some name', -2.5)

        result = component_under_test.get_jahresausgaben_nach_kategorie_prozentual(2015)

        assert set(result.keys()) == set(['kategorie 1', 'kategorie 2'])
        assert  result['kategorie 1'] == 75.00
        assert  result['kategorie 2'] == 25.00

class ausgaben_Letzten6Monate(unittest.TestCase):

    def test_withEmptyDatabase_shouldReturnListOfZeros(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.get_letzte_6_monate_ausgaben() == [0, 0, 0, 0, 0, 0]

    def test_withOnlyDataOfToday_shouldReturnSumOfMonthPaddedWithZeros(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '', '', -1.23)
        assert component_under_test.get_letzte_6_monate_ausgaben() == [0, 0, 0, 0, 0, 1.23]

class einnahmen_Letzten6Monate(unittest.TestCase):

    def test_withEmptyDatabase_shouldReturnListOfZeros(self):
        component_under_test = Einzelbuchungen()
        assert component_under_test.get_letzte_6_monate_einnahmen() == [0, 0, 0, 0, 0, 0]

    def test_withOnlyDataOfToday_shouldReturnSumOfMonthPaddedWithZeros(self):
        component_under_test = Einzelbuchungen()
        component_under_test.add(date.today(), '', '', 1.23)
        assert component_under_test.get_letzte_6_monate_einnahmen() == [0, 0, 0, 0, 0, 1.23]