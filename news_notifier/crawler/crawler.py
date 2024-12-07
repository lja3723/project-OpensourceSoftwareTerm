from abc import ABC, abstractmethod
from news_notifier.news_collector import newsapi_en_sources as sources

class CrawlerBase(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def crawler(self):
        pass


class CrawlerFactory:

    @staticmethod
    def __get_cnn_crawler(url: str) -> CrawlerBase:
        from .cnn_crawler import CnnCrawler
        return CnnCrawler(url)


    __crawlers = { "cnn": __get_cnn_crawler}

    @staticmethod
    def get_crawler(src_name: str, url: str) -> CrawlerBase:
        if src_name not in sources or src_name not in CrawlerFactory.__crawlers:
            raise ValueError("Invalid source name")

        return CrawlerFactory.__crawlers[src_name](url)