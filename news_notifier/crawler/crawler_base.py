
from abc import ABC, abstractmethod

class CrawlerBase(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def crawler(self):
        pass