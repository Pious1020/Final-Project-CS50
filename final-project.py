import os
from datetime import datetime
import requests
import sensitive



now = datetime.now()
afterdate = now.replace(hour=0, minute=0, second=0, microsecond=0)
beforedate = now.replace(hour=23, minute=59, second=59, microsecond=999999)
afterdate = afterdate.isoformat()
beforedate = beforedate.isoformat()
beforedate = beforedate + "Z"
afterdate = afterdate + "Z"

API_KEY = sensitive.API_KEY

def main():
    chromecast_name = input("Enter the name of your chromecast: ")
    channel_name = input("Enter channel name: ")
    query = input("Input what you want to search for: ")
    replaced_query = query.replace(" ", "+")
    channel_id = get_channel_id(channel_name)
    APIREQUEST = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&channelId={channel_id}&order=date&q={replaced_query}&type=video&key={API_KEY}"
    RESPONSE = requests.get(APIREQUEST, timeout=10)
    data = RESPONSE.json()
    clean_data = data_cleanup(data, query)
    filtered_sorted_data = date_sort(clean_data)
    os.system(f"catt -d \"{chromecast_name}\" set_default")
    play_video(filtered_sorted_data[0]["url"])

def get_channel_id(channel_name: str) -> str:
    channel_name = channel_name.replace(" ", "+")
    channel_search_string = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={channel_name}&key={API_KEY}&maxResults=10"
    response = requests.get(channel_search_string, timeout=10)
    channel_data = response.json()
    channel_id = channel_data['items'][0]['id']['channelId']
    return channel_id

def play_video(URl):
    os.system("catt cast " + URl)

def data_cleanup(data: list, query: str) -> list:
    filtered_data = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "")
        date = snippet.get("publishedAt", "")
        filtered_data.append(
            {
                "title": title,
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "date": date,
            }
        )
    return filtered_data

def date_sort(filtered_data: list) -> list:
    date_sorted_data = sorted(filtered_data, key=lambda x: x["date"], reverse=True)
    return date_sorted_data

if __name__ == "__main__":
    main()
