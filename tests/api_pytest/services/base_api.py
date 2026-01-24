import requests
from tests.api_pytest.utils.allure_logger import allure_attach

class BaseAPI:

    def post(self, url, headers, payload):
        response = requests.post(url, headers=headers, json=payload)
        allure_attach("POST", url, response, headers=headers, payload=payload)
        return response

    def get(self, url, headers):
        response = requests.get(url, headers=headers)
        allure_attach("GET", url, response, headers=headers)
        return response

    def put(self, url, headers, payload):
        response = requests.put(url, headers=headers, json=payload)
        allure_attach("PUT", url, response, headers=headers, payload=payload)
        return response

    def delete(self, url, headers):
        response = requests.delete(url, headers=headers)
        allure_attach("DELETE", url, response, headers=headers)
        return response
