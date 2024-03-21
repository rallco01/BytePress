from newspaper import Article

# Returns an article object
def get_article(link):  
    article = Article(link)
    article.download()
    article.parse()

    return article

# returns the content of the article as HTML paragraph items
def content_to_html(article):   
    content = article.text
    content_split = content.split('\n')

    def get_authors_str():
        authors = ""
        for author in article.authors:
            authors = f'{authors}{author}, '
        return authors[:-2]

    html_content = f'<section class="chapter">\n<h1>{article.title}</h1>\n<h2>{get_authors_str()}</h2>\n'
    for paragraph in content_split:
        html_para = f"<p>{paragraph}</p>\n"
        html_content = f'{html_content}{html_para}'
    html_content = f'{html_content}</section>\n'

    return html_content

# Returns an entire HTML page as a string
def create_html_chapter(html_content):
    html=""
    html = f'{html}<html>\n<head></head>\n<body>\n'
    html = f'{html}{html_content}'
    html = f'{html}</body>\n</html>'

    return html
# Creates a HTML file
def create_html_file(filename, html):   
    with open(filename, 'wb+') as file:
        file.write(html.encode())

# Creates full HTML newspaper
def create_html_newspaper(title, links):
    # Create html string
    html="<html>\n<head></head>\n<body>\n"
    for link in links:
        article = get_article(link.link)
        html = f'{html}{content_to_html(article)}'
    html = f'{html}</body>\n</html>'

    # Create HTML File
    filename = f"{title}.html"
    create_html_file(f".\\temp\\{filename}", html)
