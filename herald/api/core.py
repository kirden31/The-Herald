__all__ = ('BaseApiClass',)

import datetime as dt

import requests_cache


class BaseApiClass:
    base_url: str
    headers: dict

    urls_expire_after = {
        # fav
        'https://t3.gstatic.com/faviconV2': dt.timedelta(days=3),
        # newsapi
        'https://newsapi.org/v2/everything': dt.timedelta(minutes=10),
        'https://newsapi.org/v2/top-headlines': dt.timedelta(minutes=5),
        'https://newsapi.org/v2/top-headlines/sources': dt.timedelta(days=2),
        # guardian
        'https://content.guardianapis.com/search': dt.timedelta(minutes=10),
        'https://content.guardianapis.com/sections': dt.timedelta(days=2),
    }

    def __init__(self):
        self.session = requests_cache.CachedSession(
            'api/cache/http_cache',
            backend='sqlite',
            urls_expire_after=self.urls_expire_after,
            stale_if_error=True,
            ignored_parameters=['apiKey', 'api-key'],
        )

    def _request(self, endpoint='', params=None, url=None, expire_after=None):
        if not url:
            url = self.base_url + endpoint

        try:
            response = self.session.get(url, params=params, expire_after=expire_after)
            return response
        except Exception as e:
            return str(e)

    def get_json(self, endpoint, params=None):
        response = self._request(endpoint, params)
        return response.json()

    def get_fav_google(self, domain, size=128):
        url = 'https://t3.gstatic.com/faviconV2'
        params = {
            'url': domain,
            'size': size,
            'client': 'SOCIAL',
            'type': 'FAVICON',
            'fallback_opts': ','.join(('TYPE', 'SIZE', 'URL')),
        }

        response = self._request(url=url, params=params)

        return response.url
