from bs4 import BeautifulSoup
import requests
import csv
import sensitive

API_KEY = sensitive.API_KEY

response = requests.get(
    f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=sgpc%20live&eventType=completed&type=video&key={API_KEY}"
)

data = response.json()

print(data)


filtered_data = []
print(filtered_data)

for item in data.get("items", []):
    snippet = item.get("snippet", {})
    title = snippet.get("title", "")

print(title)
print(filtered_data)
print(snippet)

with open('filtered_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'url'])
    writer.writeheader()
    writer.writerows(filtered_data)