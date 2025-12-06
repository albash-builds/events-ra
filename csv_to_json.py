import csv, json

INPUT_FILE = "madrid-events.csv"
OUTPUT_FILE = "madrid-events.json"

events = []
with open(INPUT_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        events.append({
            "name": row["Event name"],
            "date": row["Date"],
            "start_time": row["Start Time"],
            "end_time": row["End Time"],
            "artists": row["Artists"],
            "venue": row["Venue"],
            "url": row["Event URL"],
            "attending": row["Number of guests attending"],
        })

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(events, out, ensure_ascii=False, indent=2)
