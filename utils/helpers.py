import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

def human_pause(min_sec=5, max_sec=10):
    pause = random.uniform(min_sec, max_sec)
    print(f"⏳ Pausing for {pause:.2f} seconds...")
    time.sleep(pause)

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}
