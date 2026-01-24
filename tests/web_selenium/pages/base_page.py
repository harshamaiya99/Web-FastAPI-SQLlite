from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def fill(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(text))

    def select_option(self, locator, text):
        element = self.find(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def check(self, locator):
        element = self.find(locator)
        if not element.is_selected():
            element.click()

    def uncheck(self, locator):
        element = self.find(locator)
        if element.is_selected():
            element.click()

    def get_text(self, locator):
        return self.find(locator).text

    def get_input_value(self, locator):
        return self.find(locator).get_attribute("value")

    def is_checked(self, locator):
        return self.find(locator).is_selected()

    def wait_for_url(self, partial_url):
        """Waits until the URL contains the specific string."""
        self.wait.until(EC.url_contains(partial_url))

    def set_value_js(self, locator, value):
        element = self.find(locator)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, str(value))

    def get_alert_text(self):
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None