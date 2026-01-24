# Bank Account Management Application

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)
![Pytest](https://img.shields.io/badge/Tests-Pytest-009688?style=flat-square&logo=pytest)
![Allure Report](https://img.shields.io/badge/Reporting-Allure-FF7700?style=flat-square&logo=allure)
![Playwright](https://img.shields.io/badge/UI_Testing-Playwright-2F80ED?style=flat-square&logo=playwright)
![Selenium](https://img.shields.io/badge/UI_Testing-Selenium-43B02A?style=flat-square&logo=selenium)
![Karate](https://img.shields.io/badge/API_Testing-Karate-ED1C24?style=flat-square&logo=karate)

## Table of Contents

*   [Overview](#overview)
*   [Features](#features)
*   [Technologies Used](#technologies-used)
*   [Project Structure](#project-structure)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Database Initialization](#database-initialization)
    *   [Running the Application](#running-the-application)
*   [API Endpoints](#api-endpoints)
    *   [Swagger UI / OpenAPI Documentation](#swagger-ui--openapi-documentation)
*   [Frontend Interface](#frontend-interface)
*   [Database Management](#database-management)
*   [Testing](#testing)
    *   [API Testing](#api-testing)
    *   [Web UI Testing (Playwright)](#web-ui-testing-playwright)
    *   [Generating Allure Report](#generating-allure-report)
    *   [Viewing Allure Report](#viewing-allure-report)
*   [Contributing](#contributing)
*   [Acknowledgements](#acknowledgements)

---

## Overview

This project implements a comprehensive **Bank Account Management API** using **FastAPI** as the backend framework and **SQLite** for data persistence. It provides a robust set of RESTful endpoints for managing bank accounts, including creation, retrieval, updates, and deletion.

Accompanying the API is a simple web-based user interface (frontend) built with pure HTML, CSS, and JavaScript, served directly by FastAPI using Jinja2 templates. The project also features extensive automated testing, covering both API integration tests with `requests` and `pytest`, and end-to-end web UI tests using `Playwright`. Test results are meticulously captured and presented through **Allure Reports**, offering detailed insights into test execution, failures, and historical trends.

## Features

*   **Account CRUD Operations:** Full Create, Read, Update, and Delete functionality for bank accounts.
*   **FastAPI Backend:** High-performance, easy-to-use API development with automatic OpenAPI documentation.
*   **SQLite Database:** Lightweight and serverless database for local data storage.
*   **Simple Web UI:** Basic HTML/CSS/JS interface for interacting with the API (creating, searching, viewing, updating, deleting accounts).
*   **CORS Enabled:** Configured to allow cross-origin requests for flexible client-side integration.
*   **Health Check Endpoint:** `/health` endpoint for monitoring API status.
*   **Comprehensive Testing:**
    *   **API Tests:** Pytest-based tests verifying core API logic using `requests` and data-driven testing from CSV files.
    *   **Web UI (E2E) Tests:** Playwright-based tests simulating user interactions in a real browser, covering full lifecycle scenarios and negative cases.
*   **Allure Reporting:** Automated generation of rich, interactive test reports with detailed steps, request/response payloads, and history.

## Technologies Used

*   **Python 3.9+**: The core programming language for both backend and testing.
*   **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn**: An ASGI server for running FastAPI applications.
*   **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
*   **Pydantic**: Data validation and settings management using Python type hints, integral to FastAPI's request/response models.
*   **Jinja2**: A modern and designer-friendly templating language for Python, used for rendering HTML pages.
*   **Pytest**: A mature full-featured Python testing framework.
*   **Requests**: An elegant and simple HTTP library for Python, used in API tests.
*   **Playwright**: A Python library to automate Chromium, Firefox and WebKit with a single API, used for robust end-to-end web UI testing.
*   **Allure Report**: A flexible lightweight multi-language test report tool that gives a clear overview of the test execution, including trends and detailed steps.

## Project Structure

```
.
web-FastAPI-SQLlite
├── .github                                 # GitHub Actions CI/CD configuration folder
│   ├── actions                             # Custom reusable composite actions
│   │   ├── generate-report
│   │   │   └── action.yml                  # Generates Allure report & history (CI step)
│   │   ├── restore-history
│   │   │   └── action.yml                  # Downloads previous report history for trend graphs
│   │   ├── run-tests
│   │   │   └── action.yml                  # Orchestrates running API, Playwright, and Selenium tests
│   │   └── setup-env
│   │       └── action.yml                  # Sets up Python, installs dependencies & browsers
│   └── workflows
│       └── main.yml                        # The main pipeline definition (triggers on push/pull_request)
├── .gitignore                              # Files and folders to exclude from Git (e.g., __pycache__, .db)
├── README.md                               # Project documentation and setup instructions
├── conftest.py                             # Global Pytest hooks (e.g., generating reports after session)
├── project_structure.txt                   # Text file containing this file tree
├── pytest.ini                              # Pytest configuration (markers, CLI defaults, log levels)
├── requirements.txt                        # Python dependencies (FastAPI, Pytest, Selenium, Playwright, etc.)
├── src                                     # Source code for the Application Under Test (AUT)
│   ├── __init__.py
│   ├── backend                             # FastAPI backend logic
│   │   ├── __init__.py
│   │   ├── crud.py                         # CRUD functions for database interaction
│   │   ├── database.db                     # SQLite database file (binary)
│   │   ├── database.py                     # Database connection and session setup
│   │   ├── main.py                         # Application entry point (uvicorn start)
│   │   ├── models.py                       # SQLAlchemy database models and Pydantic schemas
│   │   └── routes.py                       # API endpoint definitions (GET, POST, PUT, DELETE)
│   └── frontend                            # Static HTML frontend files
│       ├── accountDetails.html             # Page for viewing/updating account details
│       ├── createAccount.html              # Page for creating a new bank account
│       └── index.html                      # Landing page / Search dashboard
└── tests                                   # The Test Automation Framework
    ├── api                                 # API Testing Suite (Requests + Pytest)
    │   ├── conftest.py                     # API-specific fixtures (client setup)
    │   ├── data                            # Test Data
    │   │   ├── accounts.csv                # Positive test scenarios data
    │   │   └── accounts_negative.csv       # Negative test scenarios data
    │   ├── services                        # Service Object Model (API Wrappers)
    │   │   ├── accounts_api.py             # Wrapper methods for /accounts endpoints
    │   │   └── base_api.py                 # Base wrapper for HTTP requests
    │   ├── test_accounts_api.py            # Positive API tests
    │   ├── test_accounts_api_negative.py   # Negative API tests (error codes)
    │   └── utils                           # API Utilities
    │       ├── allure_logger.py            # Helpers for detailed Allure logging
    │       ├── csv_reader.py               # Utility to read CSV data
    │       ├── expected_response.py        # Expected JSON schemas/responses
    │       └── validators.py               # JSON schema validation logic
    ├── reports                             # Directory where local test reports are stored
    ├── web_playwright                      # UI Testing Suite (Playwright + Pytest)
    │   ├── __init__.py
    │   ├── conftest.py                     # Playwright fixtures (page injection, screenshots)
    │   ├── data
    │   │   ├── test_data.csv               # UI Positive test data
    │   │   └── test_data_negative.csv      # UI Negative test data
    │   ├── pages                           # Page Object Model (Playwright)
    │   │   ├── __init__.py
    │   │   ├── base_page.py                # Base wrapper for Playwright actions
    │   │   ├── create_page.py              # Logic for Create Account page
    │   │   ├── details_page.py             # Logic for Details/Update page
    │   │   └── home_page.py                # Logic for Home/Search page
    │   ├── test_e2e_flow.py                # Full CRUD End-to-End test (Playwright)
    │   ├── test_negative.py                # Negative UI scenarios (Playwright)
    │   └── utils
    │       ├── __init__.py
    │       ├── alert_handler.py            # Async listener for browser alerts
    │       ├── assertion_logger.py         # "Expected vs Actual" custom loggers
    │       └── csv_reader.py               # Reused CSV reader
    └── web_selenium                        # UI Testing Suite (Selenium + Pytest)
        ├── __init__.py
        ├── conftest.py                     # Selenium fixtures (Driver setup, Headless config)
        ├── data
        │   └── test_data.csv               # Data reused/copied from web_playwright
        ├── pages                           # Page Object Model (Selenium)
        │   ├── __init__.py
        │   ├── base_page.py                # Base wrapper (Explicit Waits, Find, Click)
        │   ├── create_page.py              # Selenium implementation of Create Page
        │   ├── details_page.py             # Selenium implementation of Details Page (JS Date fix)
        │   └── home_page.py                # Selenium implementation of Home Page
        ├── test_e2e_flow.py                # Full CRUD End-to-End test (Selenium version)
        └── utils
            ├── __init__.py
            ├── alert_handler.py            # Synchronous alert handling logic
            ├── assertion_logger.py         # Reused assertion logic
            └── csv_reader.py               # Reused CSV reader
```

## Getting Started

Follow these steps to set up and run the Bank Account Management API locally.

### Prerequisites

*   **Python 3.9+**
*   **pip** (Python package installer)
*   **Node.js & npm** (required by Playwright to install browser binaries)

### Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository-url>
    cd web_playwright-FastAPI-SQLlite
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install project dependencies:**

    Create a `requirements.txt` file in the root of your project with the following content:

    ```
    fastapi==0.100.0
    uvicorn[standard]
    pydantic
    Jinja2
    pytest
    requests
    allure-pytest
    playwright
    ```

    Then install:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browser binaries:**

    ```bash
    playwright install
    ```

### Database Initialization

The project uses SQLite, and the database schema is automatically created if it doesn't exist when `database.py` is run.

```bash
python src/backend/database.py
```
This will create a `database.db` file within the `src/backend/` directory if it doesn't already exist, and set up the necessary `accounts` table.

### Running the Application

To start the FastAPI application:

```bash
uvicorn src.backend.main:app --host 0.0.0.0 --port 9000 --reload
```

*   `--host 0.0.0.0`: Makes the server accessible from other machines on the network (useful for Docker or external testing).
*   `--port 9000`: Runs the application on port 9000.
*   `--reload`: Enables auto-reloading of the server on code changes during development.

The API will be accessible at `http://127.0.0.1:9000`.

## API Endpoints

The API provides the following endpoints for managing bank accounts:

| Method | Endpoint                    | Description                                  | Request Body (Example)                                     | Response Body (Example)                                     |
| :----- | :-------------------------- | :------------------------------------------- | :--------------------------------------------------------- | :---------------------------------------------------------- |
| `GET`  | `/health`                   | Checks the health status of the API.         | `N/A`                                                      | `{"status": "healthy"}`                                     |
| `GET`  | `/`                         | Serves the main HTML home page.              | `N/A`                                                      | HTML content                                                |
| `GET`  | `/createAccount.html`       | Serves the HTML page for creating accounts.  | `N/A`                                                      | HTML content                                                |
| `GET`  | `/accountDetails.html`      | Serves the HTML page for account details.    | `N/A`                                                      | HTML content                                                |
| `GET`  | `/accounts`                 | Retrieves a list of all bank accounts.       | `N/A`                                                      | `[{"account_id": "...", "account_holder_name": "...", ...}]` |
| `POST` | `/accounts`                 | Creates a new bank account.                  | `AccountCreate` model (see below)                          | `{"account_id": "...", "message": "Account created successfully"}` |
| `GET`  | `/accounts/{account_id}`    | Retrieves details for a specific account.    | `N/A`                                                      | `AccountResponse` model (see below) or `404`                |
| `PUT`  | `/accounts/{account_id}`    | Updates details for a specific account.      | `AccountUpdate` model (see below)                          | `{"message": "Account updated successfully"}`               |
| `DELETE` | `/accounts/{account_id}`  | Deletes a specific account.                  | `N/A`                                                      | `{"message": "Account deleted successfully"}`               |

### Swagger UI / OpenAPI Documentation

FastAPI automatically generates interactive API documentation. Once the application is running, you can access it at:

*   **Swagger UI**: `http://127.0.0.1:9000/docs`
*   **ReDoc**: `http://127.0.0.1:9000/redoc`

## Frontend Interface

The application includes a minimalist web frontend to demonstrate interaction with the API:

*   **Home Page (`/`)**: Allows searching for accounts by ID and navigating to the "Create Account" page.
*   **Create Account Page (`/createAccount.html`)**: A form to submit new account details. Upon successful creation, an alert displays the new account ID.
*   **Account Details Page (`/accountDetails.html`)**: Displays comprehensive details of an account. It also allows updating existing account information or deleting the account.

## Database Management

The SQLite database file `database.db` is located in `src/backend/`. You can use any SQLite browser (e.g., [DB Browser for SQLite](https://sqlitebrowser.org/)) to inspect the database schema and data directly.

## Testing

The project is equipped with both API and Web UI tests, and uses Allure for comprehensive reporting.

### API Testing

API tests are located in `tests/api/`. They use `pytest` and the `requests` library to perform CRUD operations against the running API. Test data is driven by `tests/api/data/accounts.csv`.

To run API tests:

```bash
pytest tests/api_pytest/ --alluredir=tests/reports/allure-results
```

### Web UI Testing (Playwright)

Web UI end-to-end tests are located in `tests/web/`. They use `pytest` and `Playwright` to simulate user interactions in a browser (Chromium by default). Test data for positive scenarios is in `tests/web/data/test_data.csv`, and for negative scenarios in `tests/web/data/test_data_negative.csv`.

To run Web UI tests:

```bash
pytest tests/web_playwright/ --alluredir=tests/reports/allure-results
```

You can specify a browser (e.g., `firefox`, `webkit`) using `--browser`:

```bash
pytest tests/web_playwright/ --browser=firefox --alluredir=tests/reports/allure-results
```

### Generating Allure Report

After running your tests (API or Web UI), raw Allure results will be generated in `tests/reports/allure-results`. To generate the human-readable HTML report:

```bash
allure generate tests/reports/allure-results -o tests/reports/allure-reports --clean
```

The `--clean` flag will clean the previous report data before generating a new one, ensuring fresh results. The `conftest.py` in the root also handles copying history and generating the report automatically upon `pytest_sessionfinish`.

### Viewing Allure Report

To open the generated Allure Report in your default web browser:

```bash
allure open tests/reports/allure-reports
```

This will launch a local web server to host the report, allowing you to browse test results, statistics, and trends.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and ensure tests pass.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## Acknowledgements

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [SQLite](https://www.sqlite.org/index.html)
*   [Pytest](https://pytest.org/)
*   [Playwright](https://playwright.dev/python/)
*   [Allure Report](https://allurereport.org/)
*   [Pydantic](https://pydantic-docs.helpmanual.io/)
*   [Jinja2](https://jinja.palletsprojects.com/)