from services.event_extractor import EventExtractor
from config import COHERE_API_KEY, URL_JSON_PATH, OUTPUT_JSON, OUTPUT_EXCEL

def main():
    extractor = EventExtractor(api_key=COHERE_API_KEY)
    extractor.load_urls(URL_JSON_PATH)
    extractor.extract_all_events()
    extractor.save_results(OUTPUT_JSON, OUTPUT_EXCEL)

if __name__ == "__main__":
    main()
