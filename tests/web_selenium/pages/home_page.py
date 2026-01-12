import allure
from tests.web_selenium.pages.base_page import BasePage

class HomePage(BasePage):
    URL = "" # Injected by fixture

    # Selectors
    SEARCH_INPUT = "#accountId"
    SEARCH_BTN = "button.btn-search"
    CREATE_BTN = "button.btn-create"
    ERROR_MSG = "#errorMessage"

    @allure.step("Navigate to Home Page")
    def navigate_to_home(self):
        self.navigate(self.URL)

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Search for Account")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, account_id)
        self.click(self.SEARCH_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)