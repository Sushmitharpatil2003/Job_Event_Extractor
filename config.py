from datetime import datetime

# Keys
SERPAPI_KEY = "19ca79f3c939d9648df6f06a2ab47208aaedc7e91054dcea450c2d41a67f397d"
COHERE_API_KEY = "0QN0RcpBkIfA1PNfGDOfMMRtU5kOcJLAq6jtRTVT"

# Date Config
current_year = datetime.now().year
current_month = datetime.now().strftime("%B")

# Search Queries
QUERIES = [
    f"{current_month} {current_year} job fair event site:.in",
    f"{current_month} {current_year} IT recruitment drive site:.in",
    f"{current_month} {current_year} campus hiring event site:.in",
    f"{current_month} {current_year} walk-in interview schedule site:.in",
    f"{current_month} {current_year} virtual career expo site:.in",
    f"{current_month} {current_year} online job event site:.in"
]

# File Paths
URL_JSON_PATH = "data/event_urls_serpapi.json"
URL_EXCEL_PATH = "data/event_urls_serpapi.xlsx"
OUTPUT_JSON = "data/extracted_upcoming_events.json"
OUTPUT_EXCEL = "data/extracted_upcoming_events.xlsx"
