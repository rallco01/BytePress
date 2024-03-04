This is still a Work in Progress project, progress can be viewed here: https://trello.com/b/BJHRUKuY

# About
BytePress is currently being developed as a companion app for the Kindle.

It's purpose is to conveniently allow users to download collections of articles from various RSS Sources (referred to as 'Newspapers'), I plan to add support for various different digital formats including PDF, HTML, and EPUB. 

I also plan on making this app more user friendly by creating a GUI, adding support for the filtering and frequency options currently in the newspaper JSON source, as well as by developing further features.

In it's current stage, BytePress can read RSS Feeds, retrieve articles, and package them into as many newspapers as is included in the Newspaper JSON.

# Technical
This project is written in Python as it's a user-friendly language and is easy to learn, allowing it to be customised without needing to learn a complex language. Another benefit of using Python are the libraries created for it.

Libraries used for this project are:\n
Newspaper - Codelucas (+82 contributors) - Article Extraction
ebooklib -  Aleksandar Erkalovic - Ebook Creation
Feedparser - Kurt McKee - RSS Reading

Any future GUI will probably be developed as a separate 'app' with the python code running as a background service. This may be written in a different language.
