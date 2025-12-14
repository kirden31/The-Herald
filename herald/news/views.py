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
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.TopHeadlinesFilterForm(request.GET or None)

        all_forms = (search_form, filters_form)

        if all(form.is_valid() for form in all_forms):
            params = {
                'q': search_form.cleaned_data.get('query'),
                'country': ','.join(filters_form.cleaned_data.get('country')),
                'category': ','.join(filters_form.cleaned_data.get('category')),
                'sources': filters_form.cleaned_data.get('sources'),
            }
        else:
            params = {'q': self.default_query}

        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
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
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.EverythingFiltersForm(request.GET or None)

        all_forms = (search_form, filters_form)

        if all(form.is_valid() for form in all_forms):
            params = {
                'q': search_form.cleaned_data.get('query'),
                'searchIn': ','.join(filters_form.cleaned_data.get('search_in')),
                'sources': ','.join(filters_form.cleaned_data.get('sources')),
                'from': filters_form.cleaned_data.get('_from'),
                'to': filters_form.cleaned_data.get('to'),
                'language': ','.join(filters_form.cleaned_data.get('language')),
            }
        else:
            params = {'q': self.default_query}

        endpoint = 'everything'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
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
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.GuardianFiltersForm(request.GET or None)

        all_forms = (search_form, filters_form)

        if all(form.is_valid() for form in all_forms):
            params = {
                'q': search_form.cleaned_data.get('query'),
                'section': '|'.join(filters_form.cleaned_data.get('section_or')),
                'star-rating': filters_form.cleaned_data.get('star_rating'),
                'from-date': filters_form.cleaned_data.get('_from'),
                'to-date': filters_form.cleaned_data.get('to'),
                'use-date': filters_form.cleaned_data.get('use_date'),
            }

            params = {k: v for k, v in params.items() if v}

        else:
            params = {'q': self.default_query}

        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'news': news_list,
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
        search_form = news.forms.SearchForm(request.GET or None)
        filters_form = news.forms.SourcesFilterForm(request.GET or None)

        all_forms = (search_form, filters_form)

        if all(form.is_valid() for form in all_forms):
            params = {
                'q': search_form.cleaned_data.get('query'),
                'country': ','.join(filters_form.cleaned_data.get('country')),
                'category': ','.join(filters_form.cleaned_data.get('category')),
                'language': ','.join(filters_form.cleaned_data.get('language')),
            }
        else:
            params = {'q': self.default_query}

        response = api.newsApi.NewsApi().get_sources_list(params=params)

        sources_list = response.get('sources', [])

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'sources': sources_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )
