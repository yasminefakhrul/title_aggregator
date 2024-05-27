import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_the_verge():
    url = 'https://www.theverge.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    for article in soup.find_all('h2', class_='c-entry-box--compact__title'):
        title = article.get_text()
        link = article.find('a')['href']
        date_text = article.find_previous('time')['datetime']
        date = datetime.fromisoformat(date_text.replace('Z', '+00:00'))
        
        if date >= datetime(2022, 1, 1):
            articles.append({'title': title, 'link': link, 'date': date})
    
    return sorted(articles, key=lambda x: x['date'], reverse=True)

articles = scrape_the_verge()

html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Title Aggregator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #fff;
            color: #000;
            margin: 0;
            padding: 20px;
        }}
        a {{
            text-decoration: none;
            color: #000;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .article {{
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <h1>Article Titles from The Verge</h1>
    {articles}
</body>
</html>
'''

article_template = '<div class="article"><a href="{link}">{title}</a></div>'
articles_html = '\n'.join([article_template.format(link=article['link'], title=article['title']) for article in articles])

final_html = html_template.format(articles=articles_html)

with open('title_aggregator.html', 'w') as file:
    file.write(final_html)
