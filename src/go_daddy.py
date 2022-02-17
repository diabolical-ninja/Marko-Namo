"""General Client for interacting with GoDaddy API"""

import requests
import json


class GoDaddy:
    def __init__(self, key: str, secret: str, env: str = "PROD") -> None:
        self.key = key
        self.secret = secret
        self.env = env

    def check_domain_availability(
        self, domains: list, extensions: list = [".com", ".com.au"]
    ) -> dict:

        if self.env == "PROD":
            url = "https://api.godaddy.com/v1/domains/available"
        else:
            url = "https://api.ote-godaddy.com/v1/domains/available"

        params = {"checkType": "FAST"}

        domains = [
            f"{domain}{extension}" for domain in domains for extension in extensions
        ]
        payload = json.dumps(domains)

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"sso-key {self.key}:{self.secret}",
        }

        response = requests.request(
            "POST", url, headers=headers, data=payload, params=params
        )

        return response.json()
