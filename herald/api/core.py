__all__ = ('BaseApiClass',)

import requests


class BaseApiClass:
    base_url: str
    headers: dict

    def _request(self, endpoint, params=None):
        url_endpoint = self.base_url + endpoint
        try:
            response = requests.get(url_endpoint, params=params, timeout=3)
            return response.json()
        except Exception as e:
            return str(e)

    def get_list(self, endpoint, params=None):
        response = self._request(endpoint, params)
        return response
