from .article_crawler import ArticleCrawlerBase
from bs4 import BeautifulSoup as bs
import requests


class CnnArticleCrawler(ArticleCrawlerBase):

    def __init__(self, url):
        self.url = url

    def get_article(self):
        response = requests.get(self.url)

        soup = bs(response.content, 'html.parser')

        content = soup.select_one(".article__content")
        paragraphs = content.select(".paragraph")
        article_text = ' '.join([p.get_text().strip() for p in paragraphs])

        return article_text


"""
url = "https://edition.cnn.com/2024/12/01/middleeast/syrian-regime-airstrikes-opposition-forces-intl/index.html"

cnn = CnnArticleCrawler(url)

cnn_result = cnn.get_article()

cnn_result
"""