from bs4 import BeautifulSoup
import requests
import csv
import sensitive

# page_to_scrape = requests.get("http://quotes.toscrape.com")
# soup = BeautifulSoup(page_to_scrape.text, "html.parser")

# quotes = soup.find_all("span", attrs={"class":"text"})
# authors = soup.find_all("small", attrs={"class":"author"})


# file = open("quotes.csv", "w")
# writer = csv.writer(file)

# writer.writerow(["Quote", "Author"])

# for quote, author in zip(quotes, authors):
#     print(quote.text)
#     print(author.text)
#     writer.writerow([quote.text, author.text])

# file.close()


API_KEY = sensitive.API_KEY

response = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCYn6UEtQ771a_OWSiNBoG8w&order=date&q=sgpc%20live&eventType=completed&type=video&key={API_KEY}")

data = response.json()
                        
print(data)