import os
import subprocess
import shutil
import pytest
from tests.api.services.accounts_api import AccountsAPI

BASE_URL = "http://127.0.0.1:9000"


@pytest.fixture(scope="session")
def accounts_api():
    return AccountsAPI(BASE_URL)


def pytest_sessionfinish(session, exitstatus):
    """ Automatically generate Allure report after pytest execution """
    allure_cmd = shutil.which("allure")

    if not allure_cmd:
        print("\nAllure CLI not found in PATH. Skipping report generation.")
        return

    allure_results = "tests/api/reports/allure-results"
    allure_report = "tests/api/reports/allure-reports"

    if os.path.exists(allure_results):
        subprocess.run(
            [
                allure_cmd,
                "generate",
                allure_results,
                "--clean",
                "--single-file",
                "-o",
                allure_report
            ],
            check=False
        )
        print(f"\nAllure report generated at: {allure_report}")
