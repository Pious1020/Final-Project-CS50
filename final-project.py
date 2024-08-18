import requests
import csv
import sensitive
import json
from datetime import datetime


API_KEY = sensitive.API_KEY
RESPONSE = requests.get(
    f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=sgpc%20live&eventType=completed&type=video&key={API_KEY}"
)
data = RESPONSE.json()
formatted_data = json.dumps(data, indent=2)
with open("formatted_data.json", "w") as file:
    file.write(formatted_data)


def main():
    filtered_data = filter_data(data)
    write_to_csv(filtered_data)


def filter_data(data):
    filtered_data = []
    print(filtered_data)
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")

        if "kirtan" in title.lower():
            filtered_data.append(
                {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                }
            )

def write_to_csv(filtered_data):
    for _ in len(filtered_data):
        with open("filtered_results.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "url"])
            writer.writeheader()
            writer.writerows(filtered_data)
