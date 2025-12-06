import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "madrid-events.csv"


def normalise_ra_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("http"):
        return url
    if not url.startswith("/"):
        url = "/" + url
    return "https://ra.co" + url


def get_event_image(url: str) -> str:
    url = normalise_ra_url(url)
    if not url:
        return ""

    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0 (compatible; albash-events/1.0)"}
        )
        if resp.status_code != 200:
            print(f"[warn] {url} -> {resp.status_code}")
            return ""

        soup = BeautifulSoup(resp.text, "html.parser")
        meta = soup.find("meta", property="og:image")
        if meta and meta.get("content"):
            return meta["content"]
    except Exception as e:
        print(f"[error] {url}: {e}")

    return ""


def main():
    # Read CSV
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    # Ensure Image URL column exists
    if "Image URL" not in fieldnames:
        fieldnames.append("Image URL")

    # Fill Image URL where missing
    for row in rows:
        if row.get("Image URL"):
            continue

        event_url = row.get("Event URL", "")
        print(f"Fetching image for {event_url}")
        img = get_event_image(event_url)
        if img:
            row["Image URL"] = img

        # Be polite to RA
        time.sleep(1)

    # Write updated CSV back
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done: CSV updated with Image URL column.")


if __name__ == "__main__":
    main()
