from newsapi import NewsApiClient
from src.util import jsonBeautifier

def fun():
    # Init
    newsapi = NewsApiClient(api_key='8af726a068d74a5588e34477b577a76d')

    # /v2/top-headlines
    # top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                           # sources='bbc-news,the-verge',
    #                                           category='business',
    #                                           language='en',
    #                                           country='us')

    top_headlines = newsapi.get_top_headlines(sources = 'bbc-news')
    jsonBeautifier.print(top_headlines)


    sources = newsapi.get_sources()
    # print(json.dumps(sources, indent=4))
    # print(sources.items())