from news_notifier.news_collector import NewsCollector
from news_notifier.kakao_api import KakaoApi
import time


def main():
    news_collector = NewsCollector()
    news_collector.collect_articles(sources=['bbc-news', 'cnn'])
    # news_collector.print_top_headlines_links('bbc-news')


if __name__ == "__main__":
    main()  # Call the main function
