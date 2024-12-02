from bs4 import BeautifulSoup as bs
import requests

class crawling:

    def __init__(self, url):
        self.url = url

    def crawler(self):
        response = requests.get(self.url)

        soup = bs(response.content, 'html.parser')

        content = soup.select_one(".article__content")
        paragraphs = content.select(".paragraph")
        article_text = ' '.join([p.get_text().strip() for p in paragraphs])

        return article_text