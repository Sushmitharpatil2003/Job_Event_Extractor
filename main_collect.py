from services.event_url_collector import EventURLCollector
from config import SERPAPI_KEY, QUERIES, URL_JSON_PATH, URL_EXCEL_PATH

def main():
    collector = EventURLCollector(api_key=SERPAPI_KEY)
    collector.collect_urls(QUERIES)
    collector.save_results(URL_JSON_PATH, URL_EXCEL_PATH)

if __name__ == "__main__":
    main()
