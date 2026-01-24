import pytest
import requests
from tests.api_pytest.services.accounts_api import AccountsAPI


# =========================================================
# Auth Helpers
# =========================================================

def get_auth_token(base_url, username, password):
    """
    Helper function to perform login and retrieve raw JWT token string.
    """
    url = f"{base_url}/token"
    # OAuth2 spec requires form-data
    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        pytest.fail(f"Auth failed for {username}. Status: {response.status_code}, Body: {response.text}")

    return response.json()["access_token"]


# =========================================================
# Token Fixtures
# =========================================================

@pytest.fixture(scope="session")
def clerk_token(base_url):
    """
    Logs in as Clerk and returns the raw token string.
    Consumes 'base_url' from root conftest.
    """
    return get_auth_token(base_url, "clerk", "clerk123")


@pytest.fixture(scope="session")
def manager_token(base_url):
    """
    Logs in as Manager and returns the raw token string.
    Consumes 'base_url' from root conftest.
    """
    return get_auth_token(base_url, "manager", "manager123")


# =========================================================
# API Client Fixtures
# =========================================================

@pytest.fixture(scope="session")
def accounts_api_clerk(base_url, clerk_token):
    """
    Returns AccountsAPI initialized with the Clerk's token.
    """
    return AccountsAPI(base_url, token=clerk_token)


@pytest.fixture(scope="session")
def accounts_api_manager(base_url, manager_token):
    """
    Returns AccountsAPI initialized with the Manager's token.
    """
    return AccountsAPI(base_url, token=manager_token)