__all__ = ('NewsApi',)

import api.core
import django.conf
import django.utils.dateparse


class NewsApi(api.core.BaseApiClass):
    base_url = 'https://newsapi.org/v2/'

    def __init__(self):
        super().__init__()

        self.api_key = django.conf.settings.NEWS_API_KEY

    def get_json(self, endpoint, params=None):
        if not params:
            params = {'apiKey': self.api_key}

        return super().get_json(endpoint, params)

    def get_news_list(self, endpoint, params=None):
        response = self.get_json(endpoint, params)

        total = response.get('totalResults', 0)

        news = [
            {
                'source': n.get('source').get('name'),
                'author': n.get('author'),
                'title': n.get('title'),
                'description': n.get('description'),
                'url': n.get('url'),
                'urlToImage': n.get('urlToImage'),
                'publishedAt': django.utils.dateparse.parse_datetime(n.get('publishedAt')),
                'content': n.get('content'),
            }
            for n in response.get('articles', [])
        ]

        return {'news': news, 'total': total}

    def get_sources_list(self, endpoint='top-headlines/sources', params=None):
        response = self.get_json(endpoint, params)

        sources = [
            {
                'id': s.get('id'),
                'name': s.get('name'),
                'description': s.get('description'),
                'url': s.get('url'),
                'urlToImage': self.get_fav_google(s.get('url')),
                'category': s.get('category'),
                'language': s.get('language'),
                'country': s.get('country'),
            }
            for s in response.get('sources', [])
        ]

        return {'sources': sources}
