import requests
import csv
import sensitive
import json
from datetime import datetime
from dateutil import parser



API_KEY = sensitive.API_KEY
RESPONSE = requests.get(sensitive.APIREQUEST)
data = RESPONSE.json()

formatted_data = json.dumps(data, indent=2)
with open("formatted_data.json", "w") as file:
    file.write(formatted_data)


def main():
    filtered_data = filter_data(data)
    print(filtered_data)
    sorted_data = date_sort(filtered_data)
    write_to_csv(sorted_data)


def filter_data(data):
    filtered_data = []
    print(filtered_data)
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        date = snippet.get("publishedAt", "")

        if "kirtan" in title.lower():
            filtered_data.append(
                {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "date" : date
                }
            )
    print(filtered_data)
    return filtered_data

def write_to_csv(sorted_data):
        with open("filtered_sorted_results.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "url", "date"])
            writer.writeheader()
            writer.writerows(sorted_data)


def date_sort(filtered_data):
    for item in filtered_data:
        date = item.get("date")
        date = parser.parse(date)
    item["date"] = date
    filtered_data.sort(key=lambda x: x["date"], reverse=False)
    return filtered_data

if __name__ == "__main__":
    main()