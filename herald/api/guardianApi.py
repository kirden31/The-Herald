__all__ = ('GuardianApi',)

import django.conf
import django.utils.dateparse

import api.core


class GuardianApi(api.core.BaseApiClass):
    base_url = 'https://content.guardianapis.com/'
    key_id = 0
    api_keys = django.conf.settings.GUARDIAN_API_KEYS

    def __init__(self):
        super().__init__()

        self.api_key = self.api_keys[self.key_id]
        self.show_fields_news = (
            'byline',
            'headline',
            'thumbnail',
            'trailText',
        )

    def get_json(self, endpoint, params=None):
        if params is None:
            params = {}

        params['api-key'] = self.api_key
        params['show-fields'] = ','.join(self.show_fields_news)

        response = super().get_json(endpoint, params)

        if self.check_api_key_limit(response.get('status_code')):
            self.api_key = self.api_keys[self.key_id]
            self.get_news_list(endpoint, params)

        return response

    def get_news_list(self, endpoint='search', params=None):
        response = self.get_json(endpoint, params)
        news = [
            {
                'source': 'Guardian',
                'author': n.get('fields').get('byline'),
                'title': n.get('webTitle'),
                'description': n.get('fields').get('headline'),
                'url': n.get('webUrl'),
                'urlToImage': n.get('fields').get('thumbnail'),
                'publishedAt': django.utils.dateparse.parse_datetime(n.get('webPublicationDate')),
                'content': n.get('fields').get('trailText'),
            }
            for n in response.get('response', {}).get('results', [])
        ]

        return {'news': news, 'pages': response.get('response', {}).get('pages', 0)}

    def get_sections_list(self, endpoint='sections', params=None):
        response = self.get_json(endpoint, params)

        sections = [
            {
                'id': s.get('id'),
                'webTitle': s.get('webTitle'),
                'webUrl': s.get('webUrl'),
                'apiUrl': s.get('apiUrl'),
            }
            for s in response.get('response', {}).get('results', [])
        ]

        return {'sections': sections}
