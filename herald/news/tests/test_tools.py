__all__ = (
    'guardian_api_data_news',
    'mocked_requests_get',
    'news_api_data_news',
    'news_api_data_sources',
)

news_api_data_news = {
    'status': 'ok',
    'totalResults': 1,
    'articles': [
        {
            'source': {'id': 'id', 'name': 'name'},
            'author': 'author',
            'title': 'title',
            'description': 'description',
            'url': 'url',
            'urlToImage': 'urlToImage',
            'publishedAt': '2025-11-17T10:00:00Z',
            'content': 'content',
        },
        {
            'source': {'id': 'id', 'name': 'name'},
            'url': 'url',
            'urlToImage': 'urlToImage',
            'publishedAt': '2025-11-17T10:00:00Z',
            'content': 'content',
        },
    ],
}

news_api_data_sources = {
    'status': 'ok',
    'sources': [
        {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'url': 'url',
            'category': 'category',
            'language': 'language',
            'country': 'country',
        },
    ],
}

guardian_api_data_news = {
    'response': {
        'status': 'ok',
        'userTier': 'userTier',
        'total': 1,
        'startIndex': 1,
        'pageSize': 10,
        'currentPage': 1,
        'pages': 1,
        'orderBy': 'newest',
        'results': [
            {
                'fields': {
                    'byline': 'byline',
                    'headline': 'headline',
                    'thumbnail': 'thumbnail',
                    'trailText': 'trailText',
                },
                'id': 'id',
                'type': 'type',
                'sectionId': 'sectionId',
                'sectionName': 'sectionName',
                'webPublicationDate': '2022-10-21T14:06:14Z',
                'webTitle': 'webTitle',
                'webUrl': 'webUrl',
                'apiUrl': 'apiUrl',
                'isHosted': 'isHosted',
                'pillarId': 'pillarId',
                'pillarName': 'pillarName',
            },
        ],
    },
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, url_data='https://cataas.com/cat'):
            self.json_data = json_data
            self.url_data = url_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def url(self):
            return self.url_data

    if args[0] == 'https://newsapi.org/v2/everything':
        return MockResponse(news_api_data_news, 200)

    elif args[0] == 'https://newsapi.org/v2/top-headlines':
        return MockResponse(news_api_data_news, 200)

    elif args[0] == 'https://newsapi.org/v2/top-headlines/sources':
        return MockResponse(news_api_data_sources, 200)

    elif args[0] == 'https://content.guardianapis.com/search':
        return MockResponse(guardian_api_data_news, 200)

    return MockResponse(None, 404)
