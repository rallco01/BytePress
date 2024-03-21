import feedparser
import json
from datetime import datetime
import os
import shutil
from src import ebook_newspaper, article_to_html, Source

# Load data from JSON files
with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

with open("newspapers.json", "r") as jsonfile:
    newspapers = json.load(jsonfile)

# Get today's date in a filename appropriate format
date = datetime.today().strftime('%d-%m-%Y')

# Create a list to store the file names of all created files
filenames = []

# get source  to each article from RSS feed
def rss_links(source):
    article_feed = feedparser.parse(source["Source"])

    num_articles = len(article_feed)
    if(num_articles > config['max_articles']) :
        num_articles = config['max_articles']

    article_sources = []

    for i in range(num_articles):
        article_source = Source.Source(source["Publisher Name"], article_feed.entries[i].link)
        article_sources.append(article_source)
    
    return article_sources

# Get a list of all sources 
def get_list_links(newspaper):
    sources = []
    for source in newspaper["Sources"]:
        sources.extend(rss_links(source))

    return sources

# Move files to appropriate location
def send_file(filename, send_to, destination):
    match send_to:
        case "Folder":
            shutil.copy(f".\\temp\\{filename}", f"{destination}\\{filename}")

def create_epub_newspaper(newspaper, send_to, destination):
    # Create expected title and filename
    title = f'{newspaper["Title"]} {date}'
    filename = f"{title}.epub"

    # Check if file exists
    if not os.path.isfile(f".\\temp\\{filename}"):
        # Create the complete list of links
        sources = get_list_links(newspaper)
        # Create ebook from all links
        ebook_newspaper.create_ebook_newspaper(newspaper, title, sources)

        filenames.append(f".\\temp\\{filename}")
    
    # Send epub to appropriate destination
    send_file(filename, send_to, destination)

def create_html_newspaper(newspaper, send_to, destination):
    # Create expected title and filename
    title = f'{newspaper["Title"]} {date}'
    filename = f"{title}.html"

    # Check if file exists
    if not os.path.isfile(f".\\temp\\{filename}"):
        # Create the complete list of links
        sources = get_list_links(newspaper)
        
        # Create HTML from all links
        article_to_html.create_html_newspaper(title, sources)

        filenames.append(f".\\temp\\{filename}")

    # Send html file to appropriate location
    send_file(filename, send_to, destination)

def create_newspapers():
    for newspaper in newspapers:
        for destination in newspaper["Destinations"]:
            match destination["Format"]:
                case "EBook":
                    create_epub_newspaper(newspaper, destination["Send To"], destination["Destination"])
                case "HTML":
                    create_html_newspaper(newspaper, destination["Send To"], destination["Destination"])

create_newspapers()

def empty_temp_folder():
    for filename in filenames:
        os.remove(filename)

empty_temp_folder()