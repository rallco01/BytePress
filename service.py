import feedparser
import json
from src import Link, ebook_newspaper

# Load data from JSON files
with open("config.json", "r") as jsonfile:
    config = json.load(jsonfile)

with open("newspapers.json", "r") as jsonfile:
    newspapers = json.load(jsonfile)

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

def create_epub_newspaper(newspaper):
    # Create the complete list of links
    links = []
    for source in newspaper["Sources"]:
        links.extend(rss_links(source))
    # Send Newspaper data and list of links to ebook_newspaper
    ebook_newspaper.create_ebook(newspaper, links)

def create_newspapers():
    for newspaper in newspapers:
        for format in newspaper["Formats"]:
            match format:
                case "Ebook":
                    create_epub_newspaper(newspaper)

create_newspapers()

# Test
# create_epub_newspaper(newspapers[1])