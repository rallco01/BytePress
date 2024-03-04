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

    html_content = ""
    for paragraph in content_split:
        html_para = f"<p>{paragraph}</p>\n"
        html_content = html_content + html_para

    return html_content

# Returns an entire HTML page as a string
def create_html_data(html_content, article):    
    def get_authors_str():
        authors = ""
        for author in article.authors:
            authors = f'{authors}{author}, '
        return authors[:-2]
    
    html=""
    html=f'{html}<html>\n<head></head>\n<body>\n<section class="page">\n'
    html=f'{html}<h1>{article.title}</h1>\n'
    html=f'{html}<h2>{get_authors_str()}</h2>\n'
    html=f'{html}{html_content}'
    html=f'{html}</body>\n</html>'

    return html

# Creates a HTML file
def create_html_file(filename, html):   
    with open(filename, 'wb+') as file:
        file.write(html.encode())