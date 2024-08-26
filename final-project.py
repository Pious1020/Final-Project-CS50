import csv
import json
import re
from datetime import datetime, time
import requests
from dateutil import parser
import sensitive
import os


now = datetime.now()
afterdate = now.replace(hour=0, minute=0, second=0, microsecond=0)
beforedate = now.replace(hour=23, minute=59, second=59, microsecond=999999)

afterdate = afterdate.isoformat()
beforedate = beforedate.isoformat()
beforedate = beforedate + "Z"
afterdate = afterdate + "Z"

API_KEY = sensitive.API_KEY
APIREQUEST = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=Official+SGPC+LIVE+%7C+Gurbani+Kirtan+%7C+Sachkhand+Sri+Harmandir+Sahib%2C+Sri+Amritsar+%7C&type=video&key={API_KEY}&publishedAfter={afterdate}&publishedBefore={beforedate}"
RESPONSE = requests.get(APIREQUEST, timeout=10)
data = RESPONSE.json()

current_time = datetime.now()
set_time = time(16, 0)


def main():
    clean_data = data_cleanup(data)
    filtered_data = filter_results_by_date(clean_data)
    filtered_sorted_data = date_sort(filtered_data)
    if current_time.time() <= set_time:
        play_video(filtered_sorted_data[0]["url"])
    else:
        play_video(filtered_sorted_data[2]["url"])

def play_video(URl):
    os.system("catt cast " + URl)

def data_cleanup(data: list) -> list:
    regularmatch = r"""Official SGPC LIVE \| Gurbani Kirtan \| Sachkhand Sri Harmandir Sahib, Sri Amritsar \| \d{2}\.\d{2}\.\d{4}"""
    filtered_data = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        date = snippet.get("publishedAt", "")
        match = re.search(
            regularmatch,
            title,
        )
        if match:
            filtered_data.append(
                {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "date": date,
                }
            )
    return filtered_data


def date_sort(filtered_data: list) -> list:
    date_sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=False)
    return date_sorted_data


def filter_results_by_date(sorted_data: list) -> list:
    today = datetime.now()
    date_filtered_data = []
    for item in sorted_data:
        item["date"] = parser.parse(item.get("date", ""))
    for item in sorted_data:
        if item["date"].date() == today.date():
            date_filtered_data.append(item)
    return date_filtered_data


def write_to_csv(json_data: list, csv_file_name: str) -> None:
    with open(f"{csv_file_name}", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "date", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(json_data)

if __name__ == "__main__":
    main()
