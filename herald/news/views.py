__all__ = ('EverythingNews', 'GuardianNews', 'TopHeadlinesNews', 'TopHeadlinesSource')

import django.http
import django.shortcuts
import django.views

import api.guardianApi
import api.newsApi
import news.forms


class NewsApiBaseView(django.views.View):
    default_query: str

    def get_query(self, form):
        if form.is_valid():
            query = form.cleaned_data.get('query', '').strip()
            if not query:
                query = self.default_query
        else:
            query = self.default_query

        return query


class TopHeadlinesNews(NewsApiBaseView):
    template_name = 'news/top_headlines_news.html'
    default_query = 'game'

    def get(self, request, *args, **kwargs):
        form = news.forms.SearchForm(request.GET or None)

        query = self.get_query(form)

        params = {'q': query}
        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'form': form,
            'news': news_list,
            'query': query,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class EverythingNews(NewsApiBaseView):
    template_name = 'news/everything_news.html'
    default_query = 'game'

    def get(self, request, *args, **kwargs):
        form = news.forms.SearchForm(request.GET or None)

        query = self.get_query(form)

        params = {'q': query}

        endpoint = 'everything'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'form': form,
            'news': news_list,
            'query': query,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class GuardianNews(NewsApiBaseView):
    template_name = 'news/guardian_news.html'
    default_query = ''

    def get(self, request, *args, **kwargs):
        form = news.forms.SearchForm(request.GET or None)

        query = self.get_query(form)

        params = {'q': query}
        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'form': form,
            'news': news_list,
            'query': query,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class TopHeadlinesSource(NewsApiBaseView):
    template_name = 'news/sources_list.html'
    default_query = ''

    def get(self, request, *args, **kwargs):
        form = news.forms.SearchForm(request.GET or None)

        query = self.get_query(form)

        params = {'q': query}
        response = api.newsApi.NewsApi().get_sources_list(params=params)

        sources_list = response.get('sources', [])

        context = {
            'form': form,
            'sources': sources_list,
            'query': query,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
