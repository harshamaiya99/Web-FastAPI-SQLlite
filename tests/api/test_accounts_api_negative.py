import os
import pytest
import allure
import requests
from tests.api.utils.csv_reader import read_csv
from tests.api.utils.expected_response import ExpectedResponse

from tests.api.utils.allure_logger import assert_json_match, allure_attach

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts_negative.csv")

test_data = read_csv(DATA_FILE)
base_url = "http://127.0.0.1:9000/accounts"

@allure.epic("Accounts API - Negative")
@allure.feature("Negative Scenarios")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["scenario"])
def test_account_crud_flow(accounts_api, row):

    if row["scenario"] == "missing fields":
        with allure.step("Create account (POST)"):
            payload = {
                "balance": float(row["balance"]),
                "status": row["status"],
                "agreed_to_terms": True
            }

            optional_fields = [
                "account_holder_name",
                "dob",
                "gender",
                "email",
                "phone",
                "address",
                "zip_code",
                "account_type",
                "services"
            ]

            missing_fields = []

            for field in optional_fields:
                if row.get(field):
                    payload[field] = row[field]
                else:
                    missing_fields.append(field)

            # Special handling for boolean string
            if row.get("marketing_opt_in"):
                payload["marketing_opt_in"] = row["marketing_opt_in"].lower() == "true"
            else:
                missing_fields.append("marketing_opt_in")

            print(missing_fields)

            create_response = requests.post(base_url, json=payload)
            allure_attach("POST", base_url, create_response, payload=payload)

            assert create_response.status_code == 422

            errors = create_response.json()["detail"]
            assert len(errors) == len(missing_fields)

            for error in errors:
                assert error["type"] == "missing"
                assert error["msg"] == "Field required"
                assert error["loc"][0] == "body"
                assert error["loc"][1] in missing_fields







