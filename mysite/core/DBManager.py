'''
Read panda files
'''

from _io import StringIO
from datetime import datetime
from mysite.core import DatabaseModule
from mysite.core import FileSystem
import pandas as pd

def read(nutzername, ausgeschlossene_kategorien):
    if not FileSystem.instance().read('../Database_' + nutzername + '.csv'):
        neue_datenbank = DatabaseModule.Database(nutzername)
        write(neue_datenbank)

    file_content = FileSystem.instance().read('../Database_' + nutzername + '.csv')

    tables = {}

    tables["einzelbuchungen"] = ""
    tables["dauerauftraege"] = ""
    tables["gemeinsamebuchungen"] = ""
    mode = "einzelbuchungen"
    for line in file_content:
        line = line.strip()
        if line == "":
            continue
        if line == 'Dauerauftraege':
            mode = 'dauerauftraege'
            continue

        if line == 'Gemeinsame Buchungen':
            mode = 'gemeinsamebuchungen'
            continue
        if not ',' in line:
            break

        tables[mode] = tables[mode] + "\n" + line

    database = DatabaseModule.Database(nutzername, ausgeschlossene_kategorien=ausgeschlossene_kategorien)

    raw_data = pd.read_csv(StringIO(tables["einzelbuchungen"]))
    database.einzelbuchungen.parse(raw_data)
    print("READER: Einzelbuchungen gelesen")

    database.dauerauftraege.parse(pd.read_csv(StringIO(tables["dauerauftraege"])))
    print("READER: Daueraufträge gelesen")

    database.gemeinsamebuchungen.parse(pd.read_csv(StringIO(tables["gemeinsamebuchungen"])))

    print('READER: Refreshe Database')
    database.refresh()
    print('READER: Refresh done')
    return database

def write(database):
    einzelbuchungen = database.einzelbuchungen.content.copy()[database.einzelbuchungen.content.Dynamisch == False]
    einzelbuchungen_raw_data = einzelbuchungen[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    content = einzelbuchungen_raw_data.to_csv(index=False)

    content += "\n Dauerauftraege \n"
    content += database.dauerauftraege.content.to_csv(index=False)

    content += "\n Gemeinsame Buchungen \n"
    content += database.gemeinsamebuchungen.content.to_csv(index=False)

    FileSystem.instance().write('../Database_' + database.name + '.csv', content)
    print("WRITER: All Saved")
