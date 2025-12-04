__all__ = ('NewsApi',)

import api.core
import api.tools
import django.conf
import django.utils.dateparse


class NewsApi(api.core.BaseApiClass):
    base_url = 'https://newsapi.org/v2/'

    def __init__(self):
        self.api_key = django.conf.settings.NEWS_API_KEY

    def get_list(self, endpoint, params=None):
        if isinstance(params, dict):
            params['apiKey'] = self.api_key

        return super().get_list(endpoint, params)

    def get_news_list(self, endpoint, params=None):
        response = self.get_list(endpoint, params)

        total = response.get('totalResults', 0)

        news = [
            {
                'source': n['source']['name'],
                'author': n['author'],
                'title': n['title'],
                'description': n['description'],
                'url': n['url'],
                'urlToImage': n['urlToImage'],
                'publishedAt': django.utils.dateparse.parse_datetime(n['publishedAt']),
                'content': n['content'],
            }
            for n in response.get('articles', [])
        ]

        return {'news': news, 'total': total}

    def get_sources_list(self, endpoint='top-headlines/sources', params=None):
        response = self.get_list(endpoint, params)

        sources = [
            {
                'id': s['id'],
                'name': s['name'],
                'description': s['description'],
                'url': s['url'],
                'urlToImage': api.tools.get_fav_google(s['url']),
                'category': s['category'],
                'language': s['language'],
                'country': s['country'],
            }
            for s in response.get('sources', [])
        ]

        return {'sources': sources}
