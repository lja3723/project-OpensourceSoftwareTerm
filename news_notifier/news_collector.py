from dotenv import load_dotenv

from newsapi import NewsApiClient
import os


newsapi_en_sources = [
    "abc-news", "abc-news-au", "al-jazeera-english", "ars-technica", "associated-press",
    "australian-financial-review", "axios", "bbc-news", "bbc-sport", "bleacher-report",
    "bloomberg", "breitbart-news", "business-insider", "buzzfeed", "cbc-news", "cbs-news",
    "cnn", "crypto-coins-news", "engadget", "entertainment-weekly", "espn", "espn-cric-info",
    "financial-post", "football-italia", "fortune", "four-four-two", "fox-news", "fox-sports",
    "google-news", "google-news-au", "google-news-ca", "google-news-in", "google-news-uk",
    "hacker-news", "ign", "independent", "mashable", "medical-news-today", "msnbc", "mtv-news",
    "mtv-news-uk", "national-geographic", "national-review", "nbc-news", "news24", "new-scientist",
    "news-com-au", "newsweek", "new-york-magazine", "next-big-future", "nfl-news", "nhl-news",
    "politico", "polygon", "recode", "reddit-r-all", "reuters", "rte", "talksport", "techcrunch",
    "techradar", "the-american-conservative", "the-globe-and-mail", "the-hill", "the-hindu",
    "the-huffington-post", "the-irish-times", "the-jerusalem-post", "the-lad-bible", "the-next-web",
    "the-sport-bible", "the-times-of-india", "the-verge", "the-wall-street-journal", "the-washington-post",
    "the-washington-times", "time", "usa-today", "vice-news", "wired"
]


class NewsCollector:
    def __init__(self):
        load_dotenv(verbose=True)
        self.newsapi = NewsApiClient(os.getenv('NEWSAPI_ORG_API_KEY'))

    def __get_top_headlines(self, sources: list[str]):
        return self.newsapi.get_top_headlines(
            language='en',
            sources=','.join(sources),
            page_size=100,
            page=1)

    def collect_articles(self, *, sources: list[str]):
        articles = []

        for article in self.__get_top_headlines(sources)['articles']:
            src_name = article['source']['id']
            url = article['url']

            from .article_crawler.article_crawler import ArticleCrawlerFactory
            print(f"Collecting from: {url} ... ", end='')
            content = ArticleCrawlerFactory.get_crawler(src_name, url).get_article()
            if content is not None:
                articles.append({
                    "url": url,
                    "source": src_name,
                    "article": content
                })
                print("Done")

        return articles

    def print_top_headlines_links(self, source: str):
        top_headlines = self.__get_top_headlines([source])
        for article in top_headlines['articles']:
            print(article['url'])


"""
collect_articles(sources: list[str]) -> list[dict]:
    지정된 뉴스 소스에서 기사를 수집하고 기사 URL, 소스 및 내용을 포함하는 사전의 목록을 반환함
    반환된 리스트의 각 dict의 구성:
        - "url": 기사 URL.
        - "source": 기사 소스 ID.
        - "article": 기사 내용.

print_top_headlines_links(source: str) -> None:
    지정된 뉴스 소스의 주요 헤드라인 URL을 출력함

사용법
-----
1. NewsCollector 초기화:
    collector = NewsCollector()

2. 지정된 소스에서 기사 수집:
    articles = collector.collect_articles(sources=['bbc-news', 'cnn'])

3. 특정 소스에서 주요 헤드라인 링크 출력:
    collector.print_top_headlines_links(source='bbc-news')
"""
