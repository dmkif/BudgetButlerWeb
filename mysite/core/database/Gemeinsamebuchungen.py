'''
Created on 28.09.2017

@author: sebastian
'''
from datetime import datetime

from pandas.core.frame import DataFrame
from mysite.core.database.DatabaseObject import DatabaseObject


class Gemeinsamebuchungen(DatabaseObject):
    content = DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])

    def parse(self, raw_table):
        raw_table['Datum'] = raw_table['Datum'].map(lambda x: datetime.strptime(x, "%Y-%m-%d").date())
        self.content = self.content.append(raw_table, ignore_index=True)
        self._sort()

    def add(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        self.content = self.content.append(row, ignore_index=True)
        self._sort()
        self.taint()

    def anteil_gemeinsamer_buchungen(self):
        anteil_gemeinsamer_buchungen = DataFrame()
        for _, row in self.content.iterrows():
            einzelbuchung = DataFrame([[row.Datum, row.Kategorie, str(row.Name) + " (noch nicht abgerechnet, von " + str(row.Person) + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            anteil_gemeinsamer_buchungen = anteil_gemeinsamer_buchungen.append(einzelbuchung, ignore_index=True)
        return anteil_gemeinsamer_buchungen

    def drop(self, indices_to_drop):
        self.content = self.content.drop(indices_to_drop, axis=0)

    def _sort(self):
        self.content = self.content.sort_values(by='Datum')

    def delete(self, einzelbuchung_index):
        self.content = self.content.drop(einzelbuchung_index)
        self.taint()

    def edit(self, index, datum, name, kategorie, wert, person):
        self.content.loc[self.content.index[[index]], 'Datum'] = datum
        self.content.loc[self.content.index[[index]], 'Wert'] = wert
        self.content.loc[self.content.index[[index]], 'Kategorie'] = kategorie
        self.content.loc[self.content.index[[index]], 'Name'] = name
        self.content.loc[self.content.index[[index]], 'Person'] = person
        self._sort()
        self.taint()

    def rename(self, old_name, new_name):
        self.content.Person = self.content.Person.map(lambda x: self._rename_value(old_name, new_name, x))
        self.taint()

    def _rename_value(self, old, new, x):
        if x == old:
            return new
        return x

    def fuer(self, person):
        return self.content[self.content.Person == person]

    def select_range(self, mindate, maxdate):
        data = self.content.copy()
        data = data[data.Datum >= mindate]
        data = data[data.Datum <= maxdate]

        new_gemeinsame_buchungen = Gemeinsamebuchungen()
        new_gemeinsame_buchungen.content = data

        return new_gemeinsame_buchungen

    def min_date(self):
        return self.content.Datum.min()

    def max_date(self):
        return self.content.Datum.max()

    def is_empty(self):
        return self.content.empty


    def get_content(self):
        result = []
        for index,row in self.content.iterrows():
            result.append({
                'Datum': row.Datum,
                'Name': row.Name,
                'Kategorie': row.Kategorie,
                'Person': row.Person,
                'Wert': row.Wert
            })
        return result
