from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.views.sparen import uebersicht_sparkontos
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.core.database.sparen.order import Order
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def generate_basic_test_context(
        kontos: Kontos = Kontos(),
        depotauszuege: Depotauszuege = Depotauszuege(),
        sparbuchungen: Sparbuchungen = Sparbuchungen(),
        order: Order = Order()
):
    return uebersicht_sparkontos.UebersichtSparkontosContext(
        kontos=kontos,
        order=order,
        depotauszuege=depotauszuege,
        sparbuchungen=sparbuchungen
    )


def test_transaction_id_should_be_in_context():
    result = uebersicht_sparkontos.handle_request(
        request=GetRequest(),
        context=generate_basic_test_context()
    )
    assert result.is_ok()
    assert result.is_transactional()


def generate_context_with_testdata():
    sparkontos = Kontos()
    sparkontos.add(kontoname='demokonto1', kontotyp=sparkontos.TYP_SPARKONTO)
    sparkontos.add(kontoname='demokonto2', kontotyp=sparkontos.TYP_DEPOT)
    sparbuchungen = Sparbuchungen()
    sparbuchungen.add(datum('01.01.2020'), 'testname', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto1')
    sparbuchungen.add(datum('01.01.2020'), 'testname', 10, sparbuchungen.TYP_ZINSEN, 'demokonto1')
    order = Order()
    order.add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin', 999)
    depotauszuege = Depotauszuege()
    depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demokonto2', 990)
    return generate_basic_test_context(
        kontos=sparkontos,
        depotauszuege=depotauszuege,
        sparbuchungen=sparbuchungen,
        order=order
    )


def test_should_list_kontos():
    result = uebersicht_sparkontos.handle_request(
        request=GetRequest(),
        context=generate_context_with_testdata()
    )

    assert result.get('sparkontos') == [
        {
            'index': 0,
            'kontoname': 'demokonto2',
            'kontotyp': 'Depot',
            'wert': '990,00',
            'aufbuchungen': '999,00',
            'difference': '-9,00',
            'difference_is_negativ': True
        },
        {
            'index': 1,
            'kontoname': 'demokonto1',
            'kontotyp': 'Sparkonto',
            'wert': '110,00',
            'aufbuchungen': '100,00',
            'difference': '10,00',
            'difference_is_negativ': False
        }
    ]

    assert result.get('gesamt') == {
        'wert': '1100,00',
        'aufbuchungen': '1099,00',
        'difference': '1,00',
        'difference_is_negativ': False
    }


def test_init_with_empty_database():
    result = uebersicht_sparkontos.handle_request(GetRequest(), generate_basic_test_context())
    assert result.is_ok()


def test_init_filled_database():
    result = uebersicht_sparkontos.handle_request(GetRequest(), generate_context_with_testdata())
    assert result.is_ok()


def test_delete():
    context = generate_context_with_testdata()
    uebersicht_sparkontos.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )
    sparkontos = context.kontos()
    assert sparkontos.select().count() == 1
    assert sparkontos.get(0) == {'Kontoname': 'demokonto2',
                                 'Kontotyp': 'Depot',
                                 'index': 0}


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_sparkontos.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_sparkontos.html']
