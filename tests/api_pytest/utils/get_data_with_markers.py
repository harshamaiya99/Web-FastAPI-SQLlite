import pytest
from tests.api_pytest.utils.csv_reader import read_csv


def get_data_with_markers(test_data_file):
    raw_data = read_csv(test_data_file)
    parametrized_data = []

    for row in raw_data:
        marks = []

        # Get tags from CSV (default to empty string if missing)
        csv_tags = row.get("tags", "").split(";")

        # Logic to apply markers based on CSV strings
        if "smoke" in csv_tags:
            marks.append(pytest.mark.smoke)
        if "sit" in csv_tags:
            marks.append(pytest.mark.sit)
        if "regression" in csv_tags:
            marks.append(pytest.mark.regression)

        # Create a pytest parameter with the row data and the list of markers
        # The 'id' argument helps to identify the test case in logs
        parametrized_data.append(
            pytest.param(row, marks=marks, id=row["account_holder_name"])
        )

    return parametrized_data

