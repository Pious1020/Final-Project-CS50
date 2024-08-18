import sensitive

import requests

API_KEY = sensitive.API_KEY
USERNAME = input("Enter the username of the channel: ")

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&forUsername={USERNAME}&key={API_KEY}"

response = requests.get(url)
data = response.json()

if 'items' in data and len(data['items']) > 0:
    channel_id = data["items"][0]["id"]
    print(f"channel_id: {channel_id}")