
from mysite.viewcore import request_handler
from mysite.viewcore.viewcore import post_action_is
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_to_german

def _handle_request(request):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    if post_action_is(request, 'delete'):
        print("Delete: ", request.values['delete_index'])
        einzelbuchungen.delete(int(request.values['delete_index']))

    db = einzelbuchungen.get_all()
    ausgaben_monatlich = {}
    datum_alt = None
    ausgaben_liste = []
    for row_index, row in db.iterrows():
        if datum_alt == None:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month or datum_alt.year != row.Datum.year:
            ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste
            ausgaben_liste = []
            datum_alt = row.Datum

        link = 'addeinnahme'
        if row.Wert < 0:
            link = 'addausgabe'
        ausgaben_liste.append({
            'index':row_index,
            'datum':datum_to_german(row.Datum),
            'name':row.Name,
            'kategorie':row.Kategorie,
            'wert':'%.2f' % row.Wert,
            'dynamisch':row.Dynamisch,
            'link':link,
            'tags':str(row.Tags)})

    if datum_alt != None:
        ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste

    context = viewcore.generate_base_context('uebersicht')
    context['alles'] = ausgaben_monatlich
    context['transaction_key'] = 'requested'
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'uebersicht.html')

