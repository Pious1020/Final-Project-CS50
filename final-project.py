import requests
import csv
import sensitive
import json
from datetime import datetime
from dateutil import parser
from chrome_casting import play_video
import re

API_KEY = sensitive.API_KEY
RESPONSE = requests.get(sensitive.APIREQUEST)
data = RESPONSE.json()

formatted_data = json.dumps(data, indent=2)
with open("formatted_data.json", "w") as file:
    file.write(formatted_data)
    print("Data written to JSON file successfully.")


def main():
    filtered_data = filter_data(data)
    sorted_data = date_sort(filtered_data)
    sorted_filtered_data = filter_results_by_date(sorted_data)
    write_to_csv(sorted_filtered_data)
    # play_video(sorted_data[0]["url"])


def filter_data(data):
    filtered_data = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        date = snippet.get("publishedAt", "")
        match = re.search(
            r"Official SGPC LIVE \| Gurbani Kirtan \| Sachkhand Sri Harmandir Sahib, Sri Amritsar \| \d{2}\.\d{2}\.\d{4}",
            title,
        )
        if match:
            print("Match found")
            filtered_data.append(
                {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "date": date,
                }
            )
    return filtered_data


def date_sort(filtered_data):
    for item in filtered_data:
        item["date"] = parser.parse(item.get("date", ""))
    sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=False)
    return sorted_data


def filter_results_by_date(sorted_data):
    print("Filtering results by date.")
    today = datetime.now()
    filtered_data = []
    for item in sorted_data:
        if item["date"].date() == today.date():
            print("Match found")
            filtered_data.append(item)
    return filtered_data

def write_to_csv(sorted_data):
    with open("filtered_sorted_data.csv", "w", newline="") as csvfile:
        fieldnames = ["title", "date", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)
        print("Data written to CSV successfully.")


# def button_click():
#     data = RESPONSE.json()
#     date = data.get("items", [])[0].get("snippet", {}).get("publishedAt", "")
#     if datetime.now().date() >= :
#         print("Button clicked")


if __name__ == "__main__":
    main()
