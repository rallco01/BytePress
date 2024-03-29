from ebooklib import epub
import json
from datetime import datetime
from . import Source
from src import article_to_html

# Returns a chapter object
def source_to_chapter(source):
    article = article_to_html.get_article(source.link)
    html_content = article_to_html.content_to_html(article)
    html_chapter = article_to_html.create_html_chapter(html_content)

    title = f'{source.publisher} : {article.title}'

    chapter = epub.EpubHtml(
        title=title,
        file_name=f"{''.join(letter for letter in title if letter.isalnum())}.xhtml",
        lang='en'
    )
    chapter.content = html_chapter

    return chapter

# Returns a list of chapter objects
def sources_to_chapters(sources):
    chapters = []
    for source in sources:
        chapters.append(source_to_chapter(source))

    return chapters

# Creates the ebook file
def create_ebook_newspaper(newspaper, title, sources):
    # Get data from newspaper object for epub
    author = newspaper["Author"]
    cover_path = newspaper["Cover Path"]

    # Create the epub
    book = epub.EpubBook()
    # Set based on config data
    book.set_identifier(title.replace(" ", "_"))
    book.set_title(title)
    book.add_author(author)
    book.set_cover(cover_path, open(cover_path, "rb").read())
    # Required for every epub
    book.set_language('en')
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    # define css style
    style = open("default_style.css", "rb").read()
    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    # create spine
    book.spine.append('cover')
    book.spine.append('nav')

    # Add chapters to the epub
    chapters = sources_to_chapters(sources)
    for chapter in chapters:
        print(chapter.title)
        book.add_item(chapter)
        book.toc.append(chapter)
        book.spine.append(chapter)
    
    epub.write_epub(f'.\\temp\\{title}.epub', book, {})