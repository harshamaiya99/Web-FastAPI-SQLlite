from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.web_selenium.utils.alert_handler import AlertHandler

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Standardize default wait
        self.wait = WebDriverWait(driver, 10)
        self.alert = AlertHandler(driver)

    def navigate(self, url):
        self.driver.get(url)

    def find(self, selector):
        """Returns a single WebElement (visible)"""
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))

    def find_all(self, selector):
        """Returns a LIST of WebElements"""
        # We don't necessarily wait for visibility of ALL, just presence is usually enough for lists
        return self.driver.find_elements(By.CSS_SELECTOR, selector)

    def click(self, selector):
        self.find(selector).click()

    def fill(self, selector, text):
        element = self.find(selector)
        element.clear()
        element.send_keys(str(text))

    def select_option(self, selector, text):
        # Selenium uses a specific Select class for <select> tags
        element = self.find(selector)
        select = Select(element)
        select.select_by_visible_text(text)

    def check(self, selector):
        """Ensures a checkbox/radio is checked"""
        element = self.find(selector)
        if not element.is_selected():
            element.click()

    def uncheck(self, selector):
        """Ensures a checkbox is unchecked"""
        element = self.find(selector)
        if element.is_selected():
            element.click()

    def get_text(self, selector):
        return self.find(selector).text

    def get_input_value(self, selector):
        return self.find(selector).get_attribute("value")

    def is_checked(self, selector):
        return self.find(selector).is_selected()

    def wait_for_url(self, partial_url):
        # Explicit wait for URL contains
        self.wait.until(EC.url_contains(partial_url))

    def set_value_js(self, selector, value):
        """
        Sets the value of an element directly using JavaScript.
        Crucial for <input type="date"> or stubborn fields that reject send_keys.
        """
        element = self.find(selector)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, str(value))

    def get_validation_message(self, selector):
        element = self.find(selector)
        return element.get_property("validationMessage")