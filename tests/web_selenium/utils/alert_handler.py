from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Callable

class AlertHandler:
    def __init__(self, driver):
        self.driver = driver

    def get_text_and_accept(self, trigger_action: Callable) -> str:
        """
        Triggers an action, waits for alert, gets text, accepts it.
        """
        # 1. Trigger the alert (e.g., click a button)
        trigger_action()

        # 2. Wait for alert to be present
        WebDriverWait(self.driver, 5).until(EC.alert_is_present())

        # 3. Switch to alert
        alert = self.driver.switch_to.alert
        text = alert.text

        # 4. Accept
        alert.accept()
        return text