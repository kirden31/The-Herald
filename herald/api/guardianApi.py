__all__ = ('GuardianApi',)

import django.conf
import django.utils.dateparse

import api.core


class GuardianApi(api.core.BaseApiClass):
    base_url = 'https://content.guardianapis.com/'

    def __init__(self):
        super().__init__()

        self.api_key = django.conf.settings.GUARDIAN_API_KEY
        self.show_fields_news = (
            'byline',
            'headline',
            'thumbnail',
            'trailText',
        )

    def get_data(self, endpoint, params=None, additional_params=None):
        if params is None:
            params = {}

        params['api-key'] = self.api_key

        if additional_params:
            for key, value in additional_params.items():
                params[key] = value

        response = self.get_json(endpoint, params)

        data = response.get('response', {})
        results = data.get('results', [])
        total = data.get('total', 0)
        current_page = data.get('currentPage', None)

        return results, total, current_page

    def get_news_list(self, endpoint='search', params=None):
        additional_params = {'show-fields': ','.join(self.show_fields_news)}

        results, total, current_page = self.get_data(endpoint, params, additional_params)

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
            for n in results
        ]

        return {'news': news, 'total': total, 'current_page': current_page}

    def get_sections_list(self, endpoint='sections', params=None):
        results, total, current_page = self.get_data(endpoint, params)

        sections = [
            {
                'id': s.get('id'),
                'webTitle': s.get('webTitle'),
                'webUrl': s.get('webUrl'),
                'apiUrl': s.get('apiUrl'),
            }
            for s in results
        ]

        return {'sections': sections, 'total': total, 'current_page': current_page}
