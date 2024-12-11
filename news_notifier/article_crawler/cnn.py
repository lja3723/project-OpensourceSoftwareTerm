from .article_crawler import ArticleCrawlerBase
from bs4 import BeautifulSoup as bs


class CnnArticleCrawler(ArticleCrawlerBase):
    def _crawling(self, soup: bs):
        content = soup.select_one(".article__content")
        paragraphs = content.select(".paragraph")
        return ' '.join([p.get_text().strip() for p in paragraphs])


"""
url = "https://edition.cnn.com/2024/12/01/middleeast/syrian-regime-airstrikes-opposition-forces-intl/index.html"

cnn = CnnArticleCrawler(url)

cnn_result = cnn.get_article()

cnn_result
"""
