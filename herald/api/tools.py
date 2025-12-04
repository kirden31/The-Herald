__all__ = ('get_fav_google',)

import requests


def get_fav_google(domain, size=128):
    url = 'https://t3.gstatic.com/faviconV2'
    params = {
        'url': domain,
        'size': size,
        'client': 'SOCIAL',
        'type': 'FAVICON',
        'fallback_opts': ','.join(('TYPE', 'SIZE', 'URL')),
    }

    response = requests.get(url, params=params)

    return response.url
