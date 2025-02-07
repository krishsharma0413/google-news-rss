import feedparser

topic = input("Enter a topic: ")
time = input("Enter a time: ")
url = f"https://news.google.com/rss/search?q={topic}+when:{time}d&hl=en-IN&gl=IN&ceid=IN:en"

feed = feedparser.parse(url)

def cleaner(word):
    word = str(word)
    return word.replace("‘", '"').replace("’", '"').replace("“", '"').replace("”", '"').replace("–", "-").replace("…", "...")

data = [["Title", "Time", "Source", "Link"]]
count = 0
if feed.status == 200:
    for entry in feed.entries:
        count += 1
        data.append(
            [cleaner(entry.title), cleaner(entry.published), cleaner(entry.source.title), cleaner(entry.link)]
        )
        
import csv
from datetime import datetime

with open(f"googlenews-{topic}-{datetime.today().day}.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerows(data)