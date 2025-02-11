import feedparser
import ssl
import csv
from datetime import datetime, timedelta

# SSL Context Handling
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# Function to clean text
def cleaner(word):
    word = str(word)
    return word.replace("‘", '"').replace("’", '"').replace("“", '"').replace("”", '"').replace("–", "-").replace("…", "...")

# Get User Inputs
topic = input("Enter a topic: ").replace(" ", "%20")
after = input("After time (YYYY-MM-DD): ").replace(" ", "%20")
before = input("Before time (YYYY-MM-DD): ").replace(" ", "%20")
site = input("Enter a site: ").replace(" ", "%20")
bulk = input("Do you want in bulk (y/n)? ").strip().lower().replace(" ", "%20")

# Convert Strings to Date Objects
after_date = datetime.strptime(after, "%Y-%m-%d")
before_date = datetime.strptime(before, "%Y-%m-%d")

# Store Data
data = [["Title", "Time", "Source", "Link"]]

if bulk == "y":
    current_date = after_date
    while current_date <= before_date:
        formatted_date = current_date.strftime("%Y-%m-%d")
        next_day = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        
        url = f"https://news.google.com/rss/search?q={topic}+after:{formatted_date}+before:{next_day}+site:{site}&hl=en-IN&gl=IN&ceid=IN:en"
        
        feed = feedparser.parse(url)
        if feed.status == 200:
            for entry in feed.entries:
                data.append([
                    cleaner(entry.title),
                    cleaner(entry.published),
                    cleaner(entry.source.title),
                    cleaner(entry.link)
                ])
        
        current_date += timedelta(days=1)  # Move to next date

else:
    url = f"https://news.google.com/rss/search?q={topic}+after:{after}+before:{before}+site:{site}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    if feed.status == 200:
        for entry in feed.entries:
            data.append([
                cleaner(entry.title),
                cleaner(entry.published),
                cleaner(entry.source.title),
                cleaner(entry.link)
            ])

# Save Data to CSV
filename = f"googlenews-{topic}-{datetime.today().strftime('%Y-%m-%d')}-{site.replace('.','_')}.csv"
with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Data saved to {filename}")
