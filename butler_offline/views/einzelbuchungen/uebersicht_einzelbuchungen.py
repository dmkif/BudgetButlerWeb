from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import datum_to_german, from_double_to_german
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context
from butler_offline.core.time import today


def _handle_request(request):
    year = today().year
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    years = sorted(einzelbuchungen.get_jahre(), reverse=True)
    if years:
        year = years[0]

    if request.method == 'POST' and 'date' in request.values:
        year = int(float(request.values['date']))
    einzelbuchungen_filtered = einzelbuchungen.select().select_year(year).get_all_raw()

    if post_action_is(request, 'delete'):
        einzelbuchungen.delete(int(request.values['delete_index']))
        return generate_redirect_context('/uebersicht/')

    ausgaben_monatlich = {}
    datum_alt = None
    ausgaben_liste = []
    for row_index, row in einzelbuchungen_filtered.iterrows():
        if not datum_alt:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month or datum_alt.year != row.Datum.year:
            ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste
            ausgaben_liste = []
            datum_alt = row.Datum

        link = 'addeinnahme'
        if row.Wert < 0:
            link = 'addausgabe'
        ausgaben_liste.append({
            'index': row_index,
            'datum': datum_to_german(row.Datum),
            'name': row.Name,
            'kategorie': row.Kategorie,
            'wert': from_double_to_german(row.Wert),
            'dynamisch': row.Dynamisch,
            'link': link,
            'tags': str(row.Tags)})

    if datum_alt:
        ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste

    context = generate_transactional_context('uebersicht')
    context['alles'] = ausgaben_monatlich
    context['jahre'] = years
    context['selected_date'] = year
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'einzelbuchungen/uebersicht.html')


