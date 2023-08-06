from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum, dezimal_float, from_double_to_german
from butler_offline.viewcore.converter import datum_to_string, datum_to_german
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.template import fa
from butler_offline.viewcore.context.builder import TransactionalPageContext
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
import logging


class AddEinnahmeContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


def handle_request(request, context: AddEinnahmeContext) -> TransactionalPageContext:
    page_context = generate_transactional_page_context('addeinnahme')
    page_context.add('element_titel', 'Neue Einnahme')
    page_context.add('page_subtitle', 'Daten der Einnahme:')
    page_context.add('approve_title', 'Einnahme hinzufügen')

    if post_action_is(request, 'add'):
        if 'edit_index' in request.values:
            datum_object = datum(request.values['date'])
            context.einzelbuchungen().edit(
                int(request.values['edit_index']),
                datum_object,
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            non_persisted_state.add_changed_einzelbuchungen(
                {
                    'fa': fa.pencil,
                    'datum': datum_to_german(datum_object),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(dezimal_float(request.values['wert']))
                    })

        else:
            datum_object = datum(request.values['date'])
            context.einzelbuchungen().add(
                datum_object,
                request.values['kategorie'],
                request.values['name'],
                dezimal_float(request.values['wert']))
            non_persisted_state.add_changed_einzelbuchungen(
                {
                    'fa': fa.plus,
                    'datum': datum_to_german(datum_object),
                    'kategorie': request.values['kategorie'],
                    'name': request.values['name'],
                    'wert': from_double_to_german(dezimal_float(request.values['wert']))
                    })

    if post_action_is(request, 'edit'):
        logging.info('Please edit: %s', request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        selected_item = context.einzelbuchungen().get(db_index)
        selected_item['Datum'] = datum_to_string(selected_item['Datum'])
        selected_item['Wert'] = from_double_to_german(selected_item['Wert'])
        page_context.add('default_item', selected_item)
        page_context.add('bearbeitungsmodus', True)
        page_context.add('edit_index', db_index)
        page_context.add('set_kategorie', True)
        page_context.add('element_titel', 'Einnahme Nr.' + str(db_index) + ' bearbeiten')
        page_context.add('page_subtitle', 'Daten bearbeiten:')
        page_context.add('approve_title', 'Einnahme aktualisieren')

    if  not page_context.contains('default_item'):
        page_context.add('default_item', {
            'Datum': '',
            'Name': '',
            'Wert': ''
        })

    page_context.add('kategorien',
                     sorted(context.einzelbuchungen().get_kategorien_einnahmen(hide_ausgeschlossene_kategorien=True)))
    page_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_einzelbuchungen()))
    return page_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/addeinnahme.html',
        context_creator=lambda db: AddEinnahmeContext(einzelbuchungen=db.einzelbuchungen)
    )
