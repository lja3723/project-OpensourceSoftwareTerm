from newsapi import NewsApiClient
from .utils import *

newsapi = NewsApiClient(api_key='8af726a068d74a5588e34477b577a76d')

def fun():
    # Init

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(
        language='en',
        sources='bbc-news',
        #category='business',
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