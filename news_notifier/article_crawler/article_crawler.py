from abc import ABC, abstractmethod
from news_notifier.news_collector import newsapi_en_sources as sources


class ArticleCrawlerBase(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def get_article(self):
        pass


class ArticleCrawlerFactory:

    @staticmethod
    def __get_cnn_crawler(url: str) -> ArticleCrawlerBase:
        from .cnn import CnnArticleCrawler
        return CnnArticleCrawler(url)

    __crawlers = {
        "cnn": __get_cnn_crawler
    }

    @staticmethod
    def get_crawler(src_name: str, url: str) -> ArticleCrawlerBase:
        if src_name not in sources or src_name not in ArticleCrawlerFactory.__crawlers:
            raise ValueError("Invalid source name")

        return ArticleCrawlerFactory.__crawlers[src_name](url)
