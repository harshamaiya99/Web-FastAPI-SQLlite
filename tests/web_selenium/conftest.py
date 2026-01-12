import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tests.web_selenium.pages.home_page import HomePage
from tests.web_selenium.pages.create_page import CreatePage
from tests.web_selenium.pages.details_page import DetailsPage

# Read global BASE_URL (reuse existing env var or default)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:9000")


@pytest.fixture(scope="function")
def driver():
    """Setup Selenium WebDriver (Chrome)"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # Uncomment for headless
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


# --- Page Objects Fixtures ---
@pytest.fixture
def home_page(driver):
    hp = HomePage(driver)
    hp.URL = BASE_URL  # Inject base URL
    return hp


@pytest.fixture
def create_page(driver):
    return CreatePage(driver)


@pytest.fixture
def details_page(driver):
    return DetailsPage(driver)


# --- Screenshot Hook ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if 'driver' fixture is in the test
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")