import sys
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "madrid-events.csv"


def get_event_image(url: str) -> str:
    """Fetch og:image from a RA event page."""
    if not isinstance(url, str) or not url.startswith("http"):
        return ""

    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; albash-events/1.0)"}
        )
        if resp.status_code != 200:
            print(f"[warn] {url} returned {resp.status_code}")
            return ""

        soup = BeautifulSoup(resp.text, "html.parser")
        meta = soup.find("meta", property="og:image")
        if meta and meta.get("content"):
            return meta["content"]
    except Exception as e:
        print(f"[error] fetching {url}: {e}")

    return ""


def main():
    df = pd.read_csv(CSV_PATH)

    if "Image URL" not in df.columns:
        df["Image URL"] = ""

    for idx, row in df.iterrows():
        url = row.get("Event URL")
        print(f"Fetching image for: {url}")
        img = get_event_image(url)
        if img:
            df.at[idx, "Image URL"] = img
        time.sleep(1)  # be polite to RA

    df.to_csv(CSV_PATH, index=False)
    print("Done, CSV updated with Image URL column.")


if __name__ == "__main__":
    main()
