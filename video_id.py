import requests
import sensitive
import json
from final_project import data_cleanup


# Your API key
api_key = sensitive.API_KEY

# The video ID you want to get information about
video_id = 'jNQXAC9IVRw'

# Make the API request
url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'
response = requests.get(url)
response = response.json()
x = data_cleanup(response)


# Print the JSON data
print(x)
