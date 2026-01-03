import requests
from tests.api.utils.allure_logger import attach_request, attach_response

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, payload):
        url = self.base_url + endpoint
        attach_request("POST", url, payload=payload)
        response = requests.post(url, json=payload)
        attach_response(response)
        return response

    def get(self, endpoint):
        url = self.base_url + endpoint
        attach_request("GET", url)
        response = requests.get(url)
        attach_response(response)
        return response

    def put(self, endpoint, payload):
        url = self.base_url + endpoint
        attach_request("PUT", url, payload=payload)
        response = requests.put(url, json=payload)
        attach_response(response)
        return response

    def delete(self, endpoint):
        url = self.base_url + endpoint
        attach_request("DELETE", url)
        response = requests.delete(url)
        attach_response(response)
        return response
