__all__ = ('GuardianApi',)

import api.core
import django.conf
import django.utils.dateparse


class GuardianApi(api.core.BaseApiClass):
    base_url = 'https://content.guardianapis.com/'

    def __init__(self):
        self.api_key = django.conf.settings.GUARDIAN_API_KEY
        self.show_fields = (
            'byline',
            'headline',
            'thumbnail',
            'trailText',
        )

    def get_list(self, endpoint, params=None):
        if isinstance(params, dict):
            params['api-key'] = self.api_key
            params['show-fields'] = ','.join(self.show_fields)

        return super().get_list(endpoint, params)

    def get_news_list(self, endpoint, params=None):
        response = self.get_list(endpoint, params)

        data = response.get('response', {})
        results = data.get('results', [])
        total = data.get('total', 0)

        news = [
            {
                'source': 'Guardian',
                'author': n['fields']['byline'],
                'title': n['webTitle'],
                'description': n['fields']['headline'],
                'url': n['webUrl'],
                'urlToImage': n['fields']['thumbnail'],
                'publishedAt': django.utils.dateparse.parse_datetime(n['webPublicationDate']),
                'content': n['fields']['trailText'],
            }
            for n in results
        ]

        return {'news': news, 'total': total}
