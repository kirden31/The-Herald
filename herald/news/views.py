__all__ = ('EverythingNews', 'GuardianNews', 'TopHeadlinesNews', 'TopHeadlinesSource')

import api.guardianApi
import api.newsApi
import django.http
import django.shortcuts
import django.views


class TopHeadlinesNews(django.views.View):
    template_name = 'news/top_headlines_news.html'

    def get(self, request, *args, **kwargs):
        params = {'category': 'technology'}
        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        context = {'news': response.get('news', [])}

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class EverythingNews(django.views.View):
    template_name = 'news/everything_news.html'

    def get(self, request, *args, **kwargs):
        params = {'q': 'game'}
        endpoint = 'everything'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        context = {'news': response.get('news', [])}

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class GuardianNews(django.views.View):
    template_name = 'news/everything_news.html'

    def get(self, request, *args, **kwargs):
        params = {'lang': 'ru'}
        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        context = {'news': response.get('news', [])}

        return django.shortcuts.render(request, self.template_name, context)


class TopHeadlinesSource(django.views.View):
    template_name = 'sources/sources_list.html'

    def get(self, request, *args, **kwargs):
        params = {}
        response = api.newsApi.NewsApi().get_sources_list(params=params)

        context = {'sources': response.get('sources', [])}

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
