import requests
import csv
import sensitive
import json
from datetime import datetime
from dateutil import parser
from Casting import play_video



API_KEY = sensitive.API_KEY
RESPONSE = requests.get(sensitive.APIREQUEST)
data = RESPONSE.json()

formatted_data = json.dumps(data, indent=2)
with open("formatted_data.json", "w") as file:
    file.write(formatted_data)
    print("Data written to JSON file successfully.")


def main():
    filtered_data = filter_data(data)
    print(filtered_data)
    sorted_data = date_sort(filtered_data)
    write_to_csv(sorted_data)
    play_video(sorted_data[1]["url"])


def filter_data(data):
    filtered_data = []
    print(filtered_data)
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        date = snippet.get("publishedAt", "")

        if "kirtan" in title.lower() and "audio" not in title.lower():
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
        print("Data written to CSV successfully.") 


def date_sort(filtered_data):
    for item in filtered_data:
        item["date"] = parser.parse(item.get("date", ""))
    sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=False)
    print(sorted_data)
    return sorted_data

if __name__ == "__main__":
    main()