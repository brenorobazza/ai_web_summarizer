import requests
import dotenv
import os

class Brave:
    def __init__(self):
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        dotenv.load_dotenv(dotenv.find_dotenv())
        self.api_key = os.getenv("BRAVE_API_KEY")
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY not found in environment variables.")

    def _search(self, search: str):
        search_keys = "+".join(search.strip().split())
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        response = requests.get(f"{self.base_url}?q={search_keys}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_search_results(self, search: str):
        results = self._search(search)
        return results.get("web", {}).get("results", [])