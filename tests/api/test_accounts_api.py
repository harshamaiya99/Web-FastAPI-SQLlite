import os
import pytest
import allure
from tests.api.utils.csv_reader import read_csv

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")

test_data = read_csv(DATA_FILE)


@allure.epic("Accounts API")
@allure.feature("CRUD Operations")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["account_holder_name"])
def test_account_crud_flow(accounts_api, row):

    with allure.step("Create account (POST)"):
        create_response = accounts_api.create_account(row)

        assert create_response.status_code == 200
        assert create_response.json()["message"] == "Account created successfully"

        account_id = create_response.json()["account_id"]

    with allure.step("Get account after creation (GET)"):
        get_response = accounts_api.get_account(account_id)

        assert get_response.status_code == 200
        assert get_response.json()["account_id"] == account_id
        assert get_response.json()["account_holder_name"] == row["account_holder_name"]
        assert get_response.json()["dob"] == row["dob"]
        assert get_response.json()["gender"] == row["gender"]
        assert get_response.json()["email"] == row["email"]
        assert get_response.json()["phone"] == row["phone"]
        assert get_response.json()["address"] == row["address"]
        assert get_response.json()["zip_code"] == row["zip_code"]
        assert get_response.json()["account_type"] == row["account_type"]
        assert get_response.json()["balance"] == float(row["balance"])
        assert get_response.json()["date_opened"] == row["date_opened"]
        assert get_response.json()["status"] == row["status"]
        assert get_response.json()["services"] == row["services"]
        assert get_response.json()["marketing_opt_in"] == bool(row["marketing_opt_in"])
        assert get_response.json()["agreed_to_terms"] == True

    with allure.step("Update account (PUT)"):
        update_response = accounts_api.update_account(row, account_id)

        assert update_response.status_code == 200
        assert update_response.json()["message"] == "Account updated successfully"

    with allure.step("Verify updated account (GET)"):
        get_updated_response = accounts_api.get_account(account_id)

        assert get_updated_response.status_code == 200
        assert get_updated_response.json()["account_id"] == account_id
        assert get_updated_response.json()["account_holder_name"] == row["updated_account_holder_name"]
        assert get_updated_response.json()["dob"] == row["updated_dob"]
        assert get_updated_response.json()["gender"] == row["updated_gender"]
        assert get_updated_response.json()["email"] == row["updated_email"]
        assert get_updated_response.json()["phone"] == row["updated_phone"]
        assert get_updated_response.json()["address"] == row["updated_address"]
        assert get_updated_response.json()["zip_code"] == row["updated_zip_code"]
        assert get_updated_response.json()["account_type"] == row["updated_account_type"]
        assert get_updated_response.json()["balance"] == float(row["updated_balance"])
        assert get_updated_response.json()["date_opened"] == row["updated_date_opened"]
        assert get_updated_response.json()["status"] == row["updated_status"]
        assert get_updated_response.json()["services"] == row["updated_services"]
        assert get_updated_response.json()["marketing_opt_in"] == bool(row["updated_marketing_opt_in"])
        assert get_updated_response.json()["agreed_to_terms"] == True

    with allure.step("Delete account (DELETE)"):
        delete_response = accounts_api.delete_account(account_id)

        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Account deleted successfully"
