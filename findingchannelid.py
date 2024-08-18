import sensitive

import requests

API_KEY = sensitive.API_KEY
USERNAME = input("Enter the handle of the channel: ")

url = f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet&forUsername={USERNAME}&key={API_KEY}"

response = requests.get(url)
data = response.json()
def findingchannelid() -> str:
    if 'items' in data and len(data['items']) > 0:
        channel_id = data["items"][0]["id"]
        return f"{USERNAME} = {channel_id}"
    else:
        print("Channel not found")
        return None
    
with open("channel_id.txt", mode="w", encoding="utf-8") as file:
    file.write(findingchannelid())