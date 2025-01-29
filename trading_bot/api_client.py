import requests
import json

class APIClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None
        }

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            params=params
        )
        return response.json()

    def post(self, endpoint, data):
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            data=json.dumps(data)
        )
        return response.json()

    def execute_trade(self, trade_details):
        return self.post("trades/execute", trade_details)