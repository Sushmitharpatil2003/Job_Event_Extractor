import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from serpapi.google_search import GoogleSearch
from utils.helpers import human_pause, get_headers

class EventURLCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.results = []
        self.seen_urls = set()

    def serpapi_search(self, query):
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "num": 20
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return [item['link'] for item in results.get('organic_results', [])]

    def extract_text_from_url(self, url):
        try:
            response = requests.get(url, headers=get_headers(), timeout=10)
            if not response.headers.get("Content-Type", "").startswith("text/html"):
                print(f"⚠️ Skipping non-HTML content: {url}")
                return ""
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style"]): tag.decompose()
            return re.sub(r'\s+', ' ', soup.get_text(separator=' ')).strip()
        except Exception as e:
            print(f"❌ Failed to extract {url}: {e}")
            return ""

    def is_likely_event_page(self, text):
        keywords = [
            "job fair", "walk-in", "hiring event", "recruitment drive",
            "career expo", "virtual job fair", "register", "registration",
            "venue", "interview date", "join us", "career opportunity", "apply now"
        ]
        return sum(kw in text.lower() for kw in keywords) >= 2

    def collect_urls(self, queries):
        for query in queries:
            print(f"\n🔍 Searching: {query}")
            urls = self.serpapi_search(query)
            human_pause()
            for url in urls:
                if url in self.seen_urls:
                    continue
                self.seen_urls.add(url)
                print(f"🌐 Checking: {url}")
                text = self.extract_text_from_url(url)
                if text and self.is_likely_event_page(text):
                    print("✅ Valid event page.")
                    self.results.append({"URL": url})
                else:
                    print("⚠️ Not valid.")
                human_pause()

    def save_results(self, json_path, excel_path):
        with open(json_path, "w") as f:
            json.dump(self.results, f, indent=2)
        pd.DataFrame(self.results).to_excel(excel_path, index=False)
        print(f"\n📁 Saved: {json_path}, {excel_path}")
