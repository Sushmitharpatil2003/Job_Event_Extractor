import json
import time
import re
import openpyxl
from datetime import datetime
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import cohere

class EventExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = cohere.Client(api_key)
        self.urls = []
        self.all_events = []

    def load_urls(self, path):
        with open(path, "r") as f:
            self.urls = json.load(f)

    def fetch_text(self, url):
        try:
            print(f"[Selenium] Fetching: {url}")
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(20)
            driver.get(url)
            time.sleep(3)
            text = driver.find_element("tag name", "body").text
            driver.quit()
            return text
        except Exception as e:
            print(f"[ERROR] Fetch failed: {e}")
            return None

    def build_prompt(self, text, url):
        return f"""
You are a helpful assistant that extracts structured job/career-related event information from web page text.

From the following content from this page: {url}

{text}

Extract only real job-related events — such as company hiring drives, walk-in interviews, job recruitments, or job fairs (only if they involve actual job opportunities).
Ignore general articles, webinars, counseling sessions, non-hiring career fairs, and content not related to jobs.

Only include events that take place in India.

Return the results in this exact JSON format:

[ 
  {{
    "event_name": "...",
    "event_date": "...",
    "event_location": "...",
    "organization": "...",
    "source_url": "..."
  }} 
]

Only return the JSON. If there are no valid job events in India, return []. 
"""

    def extract_events(self, text, url):
        try:
            prompt = self.build_prompt(text, url)
            response = self.client.chat(message=prompt)
            time.sleep(6)
            start, end = response.text.find("["), response.text.rfind("]") + 1
            if start != -1 and end != -1:
                return json.loads(response.text[start:end])
        except Exception as e:
            print(f"[ERROR] Extraction failed: {e}")
        return []

    def filter_upcoming(self, events):
        upcoming = []
        today = datetime.now().date()
        for event in events:
            try:
                date_str = event.get("event_date", "")
                if not date_str or date_str.lower() == "not specified":
                    continue
                if "to" in date_str:
                    match = re.search(r'(\d{1,2}[a-z]{2}\s\w+\s\d{4})', date_str)
                    if match:
                        date_str = match.group(1)
                event_dt = parser.parse(date_str, fuzzy=True).date()
                if event_dt >= today:
                    upcoming.append(event)
            except Exception as e:
                print(f"[SKIP] Date parse failed: {e}")
        return upcoming

    def extract_all_events(self):
        for entry in self.urls:
            url = entry["URL"]
            text = self.fetch_text(url)
            if text:
                events = self.extract_events(text, url)
                filtered = self.filter_upcoming(events)
                self.all_events.extend(filtered)
            time.sleep(1.5)

    def save_results(self, json_path, excel_path):
        with open(json_path, "w") as f:
            json.dump(self.all_events, f, indent=2)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Event Name", "Event Date", "Event Location", "Organization", "Source URL"])
        for e in self.all_events:
            ws.append([
                e.get("event_name", ""),
                e.get("event_date", ""),
                e.get("event_location", ""),
                e.get("organization", ""),
                e.get("source_url", "")
            ])
        wb.save(excel_path)
        print(f"[SAVED] {json_path} and {excel_path}")
