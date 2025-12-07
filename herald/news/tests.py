__all__ = ('NewsTest',)

import http
import unittest.mock

import django.test
import django.urls
import parameterized

import news.test_tools


class NewsTest(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            'news:everything_news',
            'news:top_headlines_news',
            'news:guardian_news',
        ],
    )
    @unittest.mock.patch(
        'requests_cache.CachedSession.get',
        side_effect=news.test_tools.mocked_requests_get,
    )
    def test_news_context(self, url, mock_get):
        response = django.test.Client().get(django.urls.reverse(url))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        context = response.context
        news_keys = context['news'][0].keys()

        self.assertEqual(
            {
                'source',
                'author',
                'title',
                'description',
                'url',
                'urlToImage',
                'publishedAt',
                'content',
            },
            set(news_keys),
        )

    @unittest.mock.patch(
        'requests_cache.CachedSession.get',
        side_effect=news.test_tools.mocked_requests_get,
    )
    def test_top_headlines_sources_context(self, mock_get):
        response = django.test.Client().get(django.urls.reverse('news:top_headlines_sources'))

        self.assertEqual(response.status_code, http.HTTPStatus.OK)

        context = response.context
        source_keys = context.get('sources', {})[0].keys()

        self.assertEqual(
            {
                'id',
                'name',
                'description',
                'url',
                'urlToImage',
                'category',
                'language',
                'country',
            },
            set(source_keys),
        )
