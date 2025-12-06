import csv
import json

INPUT_FILE = "madrid-events.csv"
OUTPUT_FILE = "madrid-events.json"

events = []
with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        events.append({
            "name": row.get("Event name", ""),
            "date": row.get("Date", ""),
            "start_time": row.get("Start Time", ""),
            "end_time": row.get("End Time", ""),
            "artists": row.get("Artists", ""),
            "venue": row.get("Venue", ""),
            "url": row.get("Event URL", ""),
            "attending": row.get("Number of guests attending", ""),
            "image": row.get("Image URL", ""),
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(events, out, ensure_ascii=False, indent=2)
