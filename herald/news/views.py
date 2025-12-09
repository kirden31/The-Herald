__all__ = ('EverythingNews', 'GuardianNews', 'TopHeadlinesNews', 'TopHeadlinesSource')

import django.http
import django.shortcuts
import django.views

import api.guardianApi
import api.newsApi
import news.forms


class TopHeadlinesNews(django.views.View):
    template_name = 'news/top_headlines_news.html'

    def get(self, request, *args, **kwargs):
        params = {'category': 'health'}
        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        context = {
            'news': response.get('news', []),
            'form': news.forms.SearchForm(request.GET or None),
        }

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
        params = {}
        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        context = {'news': response.get('news', [])}

        return django.shortcuts.render(request, self.template_name, context)


class TopHeadlinesSource(django.views.View):
    template_name = 'news/sources_list.html'

    def get(self, request, *args, **kwargs):
        params = {}
        response = api.newsApi.NewsApi().get_sources_list(params=params)

        context = {'sources': response.get('sources', [])}

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
