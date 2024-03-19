import feedparser
import json
from datetime import datetime
import os
import shutil
from src import Link, ebook_newspaper

# Load data from JSON files
with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

with open("newspapers.json", "r") as jsonfile:
    newspapers = json.load(jsonfile)

# Create a list to store the file names of all created files
filenames = []

# get links to each article from RSS feed
def rss_links(source):
    article_feed = feedparser.parse(source["Source"])

    num_articles = len(article_feed)
    if(num_articles > config['max_articles']) :
        num_articles = config['max_articles']

    article_links = []

    for i in range(num_articles):
        link = Link.Link(source["Publisher Name"], article_feed.entries[i].link)
        article_links.append(link)
    
    return article_links

def create_epub_newspaper(newspaper, send_to, destination):
    # Create expected title
    date = datetime.today().strftime('%d-%m-%Y')
    title = f'{newspaper["Title"]} {date}'
    # Check if file exists
    if not os.path.isfile(f".\\temp\\{title}.epub"):
        # Create the complete list of links
        links = []
        for source in newspaper["Sources"]:
            links.extend(rss_links(source))
        # Send Newspaper data and list of links to ebook_newspaper
        ebook_newspaper.create_ebook(newspaper, title, links)

        filenames.append(f".\\temp\\{title}.epub")
    
    # Send epub to appropriate destination
    match send_to:
        case "Folder":
            shutil.copy(f".\\temp\\{title}.epub", f"{destination}\\{title}.epub")

def create_newspapers():
    for newspaper in newspapers:
        print("cycling through newspapers")
        for destination in newspaper["Destinations"]:
            print("cycling through destinations")
            match destination["Format"]:
                case "EBook":
                    print("creating ebook")
                    create_epub_newspaper(newspaper, destination["Send To"], destination["Destination"])

create_newspapers()

def empty_temp_folder():
    for filename in filenames:
        os.remove(filename)

empty_temp_folder()