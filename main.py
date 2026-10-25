import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class TestUrbanRoutes:

    def setup_method(self):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def _setup_basic_route_and_taxi(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_call_taxi()
        self.routes_page.select_comfort_tariff()

    # 1. Ruta
    def test_set_route(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        assert self.routes_page.get_from() == data.address_from
        assert self.routes_page.get_to() == data.address_to

    # 2. Comfort
    def test_select_comfort_tariff(self):
        self.routes_page.set_route(data.address_from, data.address_to)
        self.routes_page.click_call_taxi()
        self.routes_page.select_comfort_tariff()
        assert self.routes_page.get_comfort_text() == "Comfort"

    # 3. Teléfono
    def test_fill_phone_number(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.click_phone_button()
        self.routes_page.set_phone(data.phone_number)
        self.routes_page.click_phone_next()

        # Espera explícita antes de pedir el código para que el servidor responda
        self.routes_page.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'input-container')]//input[@id='code']")
        ))

        code = helpers.retrieve_phone_code(self.driver)
        self.routes_page.set_phone_code(code)
        self.routes_page.click_confirm_phone()

        assert data.phone_number in self.routes_page.get_phone_text()

    # 4. Tarjeta
    def test_add_card(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.click_payment_method()
        self.routes_page.click_add_card()
        self.routes_page.set_card_number(data.card_number)
        self.routes_page.set_card_code(data.card_code)
        self.routes_page.click_link_card()
        self.routes_page.close_card_modal()

        assert self.routes_page.is_card_added() == True

    # 5. Mensaje
    def test_message_for_driver(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.set_message(data.message_for_driver)
        assert self.routes_page.get_message() == data.message_for_driver

    # 6. Manta y pañuelos
    def test_order_blanket_and_handkerchiefs(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.click_blanket()
        assert self.routes_page.is_blanket_selected() == True

    # 7. Dos helados
    def test_order_two_ice_creams(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.click_ice_cream()
        self.routes_page.click_ice_cream()
        assert self.routes_page.get_ice_cream_count() == '2'

    # 8. Modal final (Pedir taxi)
    def test_car_search_modal(self):
        self._setup_basic_route_and_taxi()
        self.routes_page.click_order_button()
        assert self.routes_page.is_order_modal_visible() == True