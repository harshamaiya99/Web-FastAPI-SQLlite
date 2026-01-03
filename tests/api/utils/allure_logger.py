import allure
import json

def attach_request(method, url, headers=None, payload=None):
    allure.attach(
        json.dumps(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "payload": payload
            },
            indent=2
        ),
        name="API Request",
        attachment_type=allure.attachment_type.JSON
    )

def attach_response(response):
    try:
        body = response.json()
    except ValueError:
        body = response.text

    allure.attach(
        json.dumps(
            {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body
            },
            indent=2
        ),
        name="API Response",
        attachment_type=allure.attachment_type.JSON
    )
