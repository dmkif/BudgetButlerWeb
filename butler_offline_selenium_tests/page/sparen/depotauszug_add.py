from butler_offline_selenium_tests.SeleniumTest import fill_element, click_add_button

class DepotauszugAdd:
    def __init__(self, driver):
        self.driver = driver

    def visit(self):
        self.driver.get('http://localhost:5000/add_depotauszug/')

    def add(self, datum, konto, depotwert, wert):
        fill_element(self.driver, 'datum_' + konto, datum)
        fill_element(self.driver, 'wert_' + konto + '_' + depotwert, wert)

        click_add_button(self.driver, '_' + konto)
