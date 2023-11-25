from butler_offline.viewcore.renderhelper import Betrag, BetragListe


def test_to_str():
    liste = BetragListe()
    liste.append(Betrag(1.23))
    liste.append(Betrag(2))
    assert str(liste) == 'BetragListe([1.23, 2.00])'


def test_js():
    liste = BetragListe()
    liste.append(Betrag(1.23))
    liste.append(Betrag(2))
    assert liste.js() == '[1.23, 2.00]'


def test_eq():
    assert BetragListe([Betrag(12.34), Betrag(2)]) == BetragListe([Betrag(12.34), Betrag(2)])
    assert not BetragListe([Betrag(12)]) == BetragListe()
    assert not BetragListe() == ''
