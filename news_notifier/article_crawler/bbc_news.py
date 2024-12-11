from .article_crawler import ArticleCrawlerBase
from bs4 import BeautifulSoup as bs


class BbcNewsArticleCrawler(ArticleCrawlerBase):
    def _crawling(self, soup: bs):
        blocks = soup.select('[data-component="text-block"]')
        all_text = []
        for block in blocks:
            paragraphs = block.select("p")
            block_text = ' '.join([p.get_text().strip() for p in paragraphs])
            all_text.append(block_text)

        return " ".join(all_text)
