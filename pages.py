from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Keys


class UrbanRoutesPage:
    # --- LOCALIZADORES MEJORADOS ---
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    call_a_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff = (By.XPATH, "//div[contains(@class,'tcard-title') and text()='Comfort']")
    comfort_tariff_active = (By.CSS_SELECTOR, ".tcard.active .tcard-title")

    phone_button = (By.CLASS_NAME, "np-text")
    phone_input = (By.ID, "phone")
    phone_next_button = (By.XPATH, "//button[contains(text(), 'Siguiente')]")
    phone_code_input = (By.XPATH, "//div[contains(@class, 'input-container')]//input[@id='code']")
    phone_confirm_button = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    payment_method_button = (By.CLASS_NAME, "pp-button")
    add_card_button = (By.XPATH, "//div[contains(text(), 'Agregar tarjeta')]")
    card_number_field = (By.ID, 'number')
    card_code_field = (By.XPATH, "//div[contains(@class, 'card-code-input')]//input[@id='code']")

    # Localizador robusto para el botón de enlazar tarjeta
    link_card_button = (By.CSS_SELECTOR, ".payment-picker .section.active button.button")

    # Localizador específico para cerrar el modal
    close_modal_button = (By.CSS_SELECTOR, ".payment-picker .section.active .section-close")

    message_field = (By.ID, 'comment')
    blanket_switch = (By.CLASS_NAME, "switch")
    blanket_checkbox = (By.CSS_SELECTOR, ".switch input[type='checkbox']")

    # Localizadores anclados al texto 'Helado'
    ice_cream_plus = (By.XPATH,
                      "//div[contains(@class,'r-counter-container')][.//div[text()='Helado']]//div[contains(@class,'counter-plus')]")
    ice_cream_counter = (By.XPATH,
                         "//div[contains(@class,'r-counter-container')][.//div[text()='Helado']]//div[contains(@class,'counter-value')]")

    # Botón final usando la clase smart-button
    order_button = (By.CLASS_NAME, "smart-button")
    order_modal = (By.CLASS_NAME, "order-body")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- MÉTODOS DE ACCIÓN ---
    def set_route(self, from_address, to_address):
        self.wait.until(EC.visibility_of_element_located(self.from_field)).send_keys(from_address)
        self.wait.until(EC.visibility_of_element_located(self.to_field)).send_keys(to_address)

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

    def set_phone_code(self, code):
        element = self.wait.until(EC.visibility_of_element_located(self.phone_code_input))
        element.send_keys(code)

    def click_confirm_phone(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_confirm_button)).click()

    def click_payment_method(self):
        self.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        self.wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()

    def click_add_card(self):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

    def set_card_number(self, card_number):
        self.wait.until(EC.visibility_of_element_located(self.card_number_field)).send_keys(card_number)

    def set_card_code(self, card_code):
        element = self.wait.until(EC.visibility_of_element_located(self.card_code_field))
        element.send_keys(card_code)
        element.send_keys(Keys.TAB)

    def click_link_card(self):
        self.wait.until(EC.element_to_be_clickable(self.link_card_button)).click()

    def close_card_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.close_modal_button)).click()

    def set_message(self, message):
        self.wait.until(EC.visibility_of_element_located(self.message_field)).send_keys(message)

    def click_blanket(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_switch)).click()

    def click_ice_cream(self):
        self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus)).click()

    def click_order_button(self):
        element = self.wait.until(EC.presence_of_element_located(self.order_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    # --- MÉTODOS DE VALIDACIÓN (get_ e is_) ---
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def get_comfort_text(self):
        return self.driver.find_element(*self.comfort_tariff_active).text

    def get_phone_text(self):
        return self.driver.find_element(*self.phone_button).text

    def is_card_added(self):
        # Validamos que el modal se haya cerrado (si el overlay no está visible, se agregó la tarjeta)
        try:
            overlay = self.driver.find_element(By.CLASS_NAME, "overlay")
            return not overlay.is_displayed()
        except:
            return True  # Si no encuentra el overlay, es que desapareció

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def is_blanket_selected(self):
        return self.driver.find_element(*self.blanket_checkbox).is_selected()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    def is_order_modal_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.order_modal)).is_displayed()