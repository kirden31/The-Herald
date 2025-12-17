__all__ = ('EverythingNews', 'GuardianNews', 'TopHeadlinesNews', 'TopHeadlinesSource')

import math

import django.core.paginator
import django.http
import django.shortcuts
import django.views

import api.guardianApi
import api.newsApi
import news.forms


class NewsApiBaseView(django.views.View):
    default_query = 'programming'
    page_size = 20

    def get_query(self, form):
        if form.is_valid():
            query = form.cleaned_data.get('query', '').strip()
            if not query:
                query = self.default_query
        else:
            query = self.default_query

        return query

    @staticmethod
    def get_view_pages_numbers(current, total, window=4):
        left_page = max(current - window, 1)
        right_page = min(current + window, total)
        return range(left_page, right_page + 1)


class TopHeadlinesNews(NewsApiBaseView):
    template_name = 'news/top_headlines_news.html'

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.TopHeadlinesFilterForm(request.GET or None)

        params = {
            'q': self.get_query(search_form),
            'pageSize': self.page_size,
        }

        if filters_form.is_valid():
            params.update(
                {
                    'q': search_form.cleaned_data.get('query'),
                    'country': ','.join(filters_form.cleaned_data.get('country')),
                    'category': ','.join(filters_form.cleaned_data.get('category')),
                    'sources': filters_form.cleaned_data.get('sources'),
                },
            )

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        max_page = math.ceil(response.get('total', 0) / self.page_size)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
            'max_page': max_page,
            'cur_page': cur_page,
            'pages_view_list': pages_view_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class EverythingNews(NewsApiBaseView):
    template_name = 'news/everything_news.html'

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.EverythingFiltersForm(request.GET or None)

        params = {
            'q': self.get_query(search_form),
            'pageSize': self.page_size,
        }

        if filters_form.is_valid():
            params.update(
                {
                    'searchIn': ','.join(filters_form.cleaned_data.get('search_in')),
                    'sources': ','.join(filters_form.cleaned_data.get('sources')),
                    'from': filters_form.cleaned_data.get('_from'),
                    'to': filters_form.cleaned_data.get('to'),
                    'language': ','.join(filters_form.cleaned_data.get('language')),
                },
            )

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'everything'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        max_page = math.ceil(response.get('total', 0) / self.page_size)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
            'max_page': max_page,
            'cur_page': cur_page,
            'pages_view_list': pages_view_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class GuardianNews(NewsApiBaseView):
    template_name = 'news/guardian_news.html'

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.GuardianFiltersForm(request.GET or None)

        params = {
            'q': self.get_query(search_form),
        }

        if filters_form.is_valid():
            params.update(
                {
                    'section': filters_form.cleaned_data.get('section'),
                    'star-rating': filters_form.cleaned_data.get('star_rating'),
                    'from-date': filters_form.cleaned_data.get('_from'),
                    'to-date': filters_form.cleaned_data.get('to'),
                    'use-date': filters_form.cleaned_data.get('use_date'),
                },
            )
            params = {k: v for k, v in params.items() if v}

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        max_page = response.get('pages', 0)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
            'max_page': max_page,
            'cur_page': cur_page,
            'pages_view_list': pages_view_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class TopHeadlinesSource(NewsApiBaseView):
    template_name = 'news/sources_list.html'
    default_query = ''

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.SourcesFilterForm(request.GET or None)

        params = {
            'q': self.get_query(search_form),
        }

        if filters_form.is_valid():
            params.update(
                {
                    'country': ','.join(filters_form.cleaned_data.get('country')),
                    'category': ','.join(filters_form.cleaned_data.get('category')),
                    'language': ','.join(filters_form.cleaned_data.get('language')),
                },
            )

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        response = api.newsApi.NewsApi().get_sources_list(params=params)

        sources_list = response.get('sources', [])

        max_page = math.ceil(response.get('total', 0) / self.page_size)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'sources': sources_list,
            'max_page': max_page,
            'cur_page': cur_page,
            'pages_view_list': pages_view_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
