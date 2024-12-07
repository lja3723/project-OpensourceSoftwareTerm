
from abc import ABC, abstractmethod

from news_notifier.news_collector import newsapi_en_sources as sources

class CrawlerBase(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def crawler(self):
        pass


class CrawlerFactory:
    __crawlers: dict = {}

    @staticmethod
    def get_crawler(src_name: str) -> CrawlerBase:
        if not src_name in CrawlerFactory.__crawlers.keys() and not src_name in sources:
            raise ValueError("Invalid source name")

        return CrawlerFactory.__crawlers[src_name]