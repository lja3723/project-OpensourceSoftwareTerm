from ..news_collector import newsapi_en_sources as sources
from crawler_base import CrawlerBase

class CrawlerFactory:
    __crawlers: dict = {}

    @staticmethod
    def get_crawler(src_name: str) -> CrawlerBase:
        if not src_name in CrawlerFactory.__crawlers.keys() and not src_name in sources:
            raise ValueError("Invalid source name")
        
        return CrawlerFactory.__crawlers[src_name]
