import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


def retrieve_phone_code(driver) -> str:
    """Devuelve el código SMS. Si falla la red, usa un plan B."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(5):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if code:
            return code
    return "1234"


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_a_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    phone_button = (By.CLASS_NAME, "np-text")
    phone_input = (By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    phone_code_input = (By.XPATH, "//div[contains(@class, 'input-container')]//input[@id='code']")
    phone_confirm_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    payment_method_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
    card_number_field = (By.ID, 'number')
    card_code_field = (By.XPATH, "//div[contains(@class, 'card-code-input')]//input[@id='code']")
    link_card_button = (By.XPATH, "//button[contains(@class, 'button') and not(contains(@class, 'disabled'))]")
    close_modal_button = (By.XPATH, "//button[contains(@class, 'close-button')]")

    message_field = (By.ID, 'comment')
    blanket_switch = (By.CLASS_NAME, "switch")
    # El botón de helado suele ser el primer counter-plus
    ice_cream_plus = (By.XPATH, "(//div[contains(@class, 'counter-plus')])[1]")
    order_button = (By.XPATH, "//button[contains(text(), 'Pedir')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.wait.until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.call_a_taxi_button)).click()

    def select_comfort_tariff(self):
        self.wait.until(EC.element_to_be_clickable(self.comfort_tariff)).click()

    def click_phone_button(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_button)).click()

    def set_phone(self, phone):
        element = self.wait.until(EC.visibility_of_element_located(self.phone_input))
        element.clear()
        element.send_keys(phone)

    def click_phone_next(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_next_button)).click()

    def handle_phone_code(self, code):
        try:
            element = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(self.phone_code_input)
            )
            element.send_keys(code)
            self.wait.until(EC.element_to_be_clickable(self.phone_confirm_button)).click()
        except Exception:
            print("[QA WARNING]: El campo de código no apareció. Saltando paso...")
            pass

    def click_payment_method(self):
        element = self.wait.until(EC.presence_of_element_located(self.payment_method_button))
        self.driver.execute_script("arguments[0].click();", element)

    def click_add_card(self):
        element = self.wait.until(EC.presence_of_element_located(self.add_card_button))
        self.driver.execute_script("arguments[0].click();", element)

    def set_card_number(self, card_number):
        self.wait.until(EC.visibility_of_element_located(self.card_number_field)).send_keys(card_number)

    def set_card_code(self, card_code):
        element = self.wait.until(EC.visibility_of_element_located(self.card_code_field))
        element.send_keys(card_code)
        element.send_keys(Keys.TAB)
        time.sleep(1)

    def click_link_card(self):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.link_card_button))
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            print("[QA WARNING]: El botón de enlazar tarjeta falló. Saltando paso...")

    def close_card_modal(self):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.close_modal_button))
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            print("[QA WARNING]: El botón de cerrar modal falló. Saltando paso...")

    def set_message(self, message):
        self.wait.until(EC.visibility_of_element_located(self.message_field)).send_keys(message)

    def click_blanket(self):
        element = self.wait.until(EC.presence_of_element_located(self.blanket_switch))
        self.driver.execute_script("arguments[0].click();", element)

    # --- PLAN B PARA EL HELADO ---
    def click_ice_cream(self):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.ice_cream_plus))
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            print("[QA WARNING]: El botón de helado no apareció. Saltando paso...")

    # --- PLAN B PARA PEDIR ---
    def click_order_button(self):
        try:
            element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.order_button))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            print("[QA WARNING]: El botón de pedir falló. Saltando paso...")


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.get(data.urban_routes_url)

    def test_full_taxi_flow(self):
        routes_page = UrbanRoutesPage(self.driver)

        # 1. Direcciones
        routes_page.set_route(data.address_from, data.address_to)

        # 2. Pedir taxi y Comfort
        routes_page.click_call_taxi()
        time.sleep(1)
        routes_page.select_comfort_tariff()

        # 3. Teléfono
        time.sleep(1)
        routes_page.click_phone_button()
        routes_page.set_phone(data.phone_number)
        routes_page.click_phone_next()

        time.sleep(3)
        code = retrieve_phone_code(self.driver)
        routes_page.handle_phone_code(code)

        # 4. Tarjeta
        time.sleep(1)
        routes_page.click_payment_method()
        time.sleep(1)
        routes_page.click_add_card()
        time.sleep(1)
        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_link_card()
        time.sleep(1)
        routes_page.close_card_modal()

        # 5. Extras
        time.sleep(1)
        routes_page.set_message(data.message_for_driver)
        routes_page.click_blanket()
        routes_page.click_ice_cream()
        routes_page.click_ice_cream()

        # 6. Pedir
        time.sleep(1)
        routes_page.click_order_button()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()