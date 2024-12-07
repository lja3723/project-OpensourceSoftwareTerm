from newsapi import NewsApiClient
from .utils import JsonBeautifier

newsapi = NewsApiClient(api_key='8af726a068d74a5588e34477b577a76d')
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


def fun():
    # Init

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(
        language='en',
        sources='bbc-news',
        # category='business',
        page_size=100,
        page=1)

    JsonBeautifier.toString(top_headlines)

    with open('top_headlines.json', 'w') as f:
        f.write(JsonBeautifier.toString(top_headlines))


def source_filter():
    # Init
    sources: list = newsapi.get_sources()['sources']
    source_ids = [source['id'] for source in sources if source['language'] == 'en']

    with open('sources_en.json', 'w') as f:
        f.write(JsonBeautifier.toString(source_ids))
