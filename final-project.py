import csv
import json
import re
from datetime import datetime, time
import requests
from dateutil import parser
import sensitive
from chrome_casting import play_video


now = datetime.now()
afterdate = now.replace(hour=0, minute=0, second=0, microsecond=0)

beforedate = now.replace(hour=23, minute=59, second=59, microsecond=999999)

afterdate = afterdate.isoformat()
beforedate = beforedate.isoformat()

# api request
API_KEY = sensitive.API_KEY
APIREQUEST = f" https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=Official+SGPC+LIVE+%7C+Gurbani+Kirtan+%7C+Sachkhand+Sri+Harmandir+Sahib%2C+Sri+Amritsar&eventType=completed&type=video&publishedBefore={beforedate}&publishedAfter={afterdate}key={API_KEY} "
RESPONSE = requests.get(APIREQUEST, timeout=10)
data = RESPONSE.json()

# writing data to json file
formatted_data = json.dumps(data, indent=2)
with open("formatted_data.json", "w", encoding="utf-8") as file:
    file.write(formatted_data)
    # print("Data written to JSON file successfully.")

# checking if time is after 4pm
current_time = datetime.now()
set_time = time(16, 0)





def main():
    clean_data = data_cleanup(data)
    # print(clean_data)
    filtered_data = filter_results_by_date(clean_data)
    # print("Filtered data: ")
    filtered_sorted_data = date_sort(filtered_data)
    write_to_csv(filtered_sorted_data, "filtered_sorted_data.csv")
    if current_time.time() <= set_time:
        print("It is time to play morning kirtan.")
        #play_video(filtered_sorted_data[0]["url"])
    else:
        print("It is time to play evening kirtan.")
        #play_video(filtered_sorted_data[2]["url"])


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
            # print("Match found")
            filtered_data.append(
                {
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "date": date,
                }
            )
    write_to_csv(filtered_data, "clean_data.csv")
    return filtered_data


def date_sort(filtered_data: list) -> list:
    date_sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=False)
    write_to_csv(date_sorted_data, "date_sorted_data.csv")
    return date_sorted_data


def filter_results_by_date(sorted_data: list) -> list:
    today = datetime.now().date()
    date_filtered_data = []
    print(f"{today}")

    for item in sorted_data:
        try:
            # Parse the date from the item
            item_date = parser.parse(item.get("date", "")).date()
            print(f"Checking item with date: {item_date}")  # Debugging
            if item_date == today:
                date_filtered_data.append(item)
        except ValueError as e:
            print(f"Error parsing date for item: {e}")

    print(f"Number of items after date filtering: {len(date_filtered_data)}")  # Debugging
    return date_filtered_data



def write_to_csv(json_data: list, csv_file_name: str) -> None:
    with open(f"{csv_file_name}", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "date", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(json_data)
        # print("Data written to CSV successfully.")


if __name__ == "__main__":
    main()
