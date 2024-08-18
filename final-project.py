import requests
import csv
import sensitive
import json

API_KEY = sensitive.API_KEY


response = requests.get(
    f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=sgpc%20live&eventType=completed&type=video&key={API_KEY}"
)

data = response.json()


formatted_data = json.dumps(data, indent=2)

print(formatted_data)


def calculating_start_time():
    response = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=sgpc%20live&eventType=completed&type=video&key={API_KEY}"
    )


def makingurl() -> str:
    filtered_data = []
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

        return filtered_data


with open("filtered_results.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(filtered_data)
