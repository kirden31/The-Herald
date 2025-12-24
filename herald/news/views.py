__all__ = ('EverythingNews', 'GuardianNews', 'TopHeadlinesNews', 'NewsApiSources')

from http import HTTPStatus
import math
import random

import django.contrib.auth.mixins
import django.contrib.messages
import django.http
import django.shortcuts
from django.utils.translation import gettext as _
import django.views

import api.guardianApi
import api.newsApi
import news.forms
import news.forms_data
import news.models
import news.services


class NewsApiBaseView(django.views.View):
    default_query: str
    page_size = 20

    @staticmethod
    def get_view_pages_numbers(current, total, window=4):
        left_page = max(current - window, 1)
        right_page = min(current + window, total)
        return range(left_page, right_page + 1)

    @staticmethod
    def get_random_favorite_category(request, form, query, country):
        cat = form.cleaned_data.get('category')
        if cat or query or country[-1]:
            return cat

        if request.user:
            cat = request.user.profile.favorite_categories
            if cat:
                return random.choice(cat)

        return news.forms_data.GENERAL


class TopHeadlinesNews(NewsApiBaseView):
    template_name = 'news/top_headlines_news.html'

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET)
        filters_form = news.forms.TopHeadlinesFilterForm(request.GET)

        if not (search_form.is_valid() and filters_form.is_valid()):
            django.contrib.messages.error(request, _('Forms_error'))
            context = {
                'search_form': search_form,
                'filters_form': filters_form,
                'news': [],
                'max_page': 0,
                'cur_page': 1,
                'pages_view_list': [],
            }
            return django.shortcuts.render(request, self.template_name, context)

        params = {
            'q': search_form.cleaned_data.get('query'),
            'sources': filters_form.cleaned_data.get('sources'),
            'pageSize': self.page_size,
        }

        if not params['sources']:
            params['country'] = (','.join(filters_form.cleaned_data.get('country')),)
            params['category'] = self.get_random_favorite_category(
                request,
                filters_form,
                params['q'],
                params['country'],
            )

        if params.get('sources') and (params.get('category') or params.get('country')):
            django.contrib.messages.error(
                self.request,
                _('You_cannot_select_sources_together_with_country_or_category'),
            )

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'top-headlines'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])
        if request.user:
            news_list = news.services.enrich_with_favorites(news_list, request.user)

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
    default_query = 'programming'

    def get(self, request, *_args, **_kwargs):
        search_form = news.forms.SearchForm(request.GET)
        filters_form = news.forms.EverythingFiltersForm(request.GET)
        sort_form = news.forms.SortEverythingForm(request.GET)

        if not (search_form.is_valid() and filters_form.is_valid() and sort_form.is_valid()):
            django.contrib.messages.error(request, _('Forms_error'))
            context = {
                'search_form': search_form,
                'filters_form': filters_form,
                'sort_form': sort_form,
                'news': [],
                'max_page': 0,
                'cur_page': 1,
                'pages_view_list': [],
            }
            return django.shortcuts.render(request, self.template_name, context)

        params = {
            'q': search_form.cleaned_data.get('query'),
            'sortBy': sort_form.cleaned_data.get('sort_by'),
            'searchIn': ','.join(filters_form.cleaned_data.get('search_in')),
            'sources': ','.join(filters_form.cleaned_data.get('sources')),
            'from': filters_form.cleaned_data.get('_from'),
            'to': filters_form.cleaned_data.get('to'),
            'language': ','.join(filters_form.cleaned_data.get('language')),
            'pageSize': self.page_size,
        }

        if not (params['q'] or params['sources']):
            params['q'] = self.default_query
            django.contrib.messages.warning(
                request,
                '{message}: {default_query}'.format(
                    message=_("Used_default_query"),
                    default_query=self.default_query,
                ),
            )

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'everything'
        response = api.newsApi.NewsApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])
        if request.user:
            news_list = news.services.enrich_with_favorites(news_list, request.user)

        max_page = math.ceil(response.get('total', 0) / self.page_size)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'sort_form': sort_form,
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
        search_form = news.forms.SearchForm(request.GET)
        filters_form = news.forms.GuardianFiltersForm(request.GET)
        sort_form = news.forms.SortGuardianForm(request.GET)

        if not (search_form.is_valid() and filters_form.is_valid() and sort_form.is_valid()):
            django.contrib.messages.error(request, _('Forms_error'))
            context = {
                'search_form': search_form,
                'filters_form': filters_form,
                'sort_form': sort_form,
                'news': [],
                'max_page': 0,
                'cur_page': 1,
                'pages_view_list': [],
            }
            return django.shortcuts.render(request, self.template_name, context)

        params = {
            'q': search_form.cleaned_data.get('query'),
            'order-by': sort_form.cleaned_data.get('sort_by'),
            'section': filters_form.cleaned_data.get('section'),
            'star-rating': filters_form.cleaned_data.get('star_rating'),
            'from-date': filters_form.cleaned_data.get('_from'),
            'to-date': filters_form.cleaned_data.get('to'),
            'use-date': filters_form.cleaned_data.get('use_date'),
        }

        params = {k: v for k, v in params.items() if v}

        try:
            cur_page = max(int(request.GET.get('page', '1')), 1)
        except ValueError:
            cur_page = 1

        params['page'] = cur_page

        endpoint = 'search'
        response = api.guardianApi.GuardianApi().get_news_list(endpoint, params)

        news_list = response.get('news', [])

        if request.user:
            news_list = news.services.enrich_with_favorites(news_list, request.user)

        max_page = response.get('pages', 0)
        pages_view_list = self.get_view_pages_numbers(cur_page, max_page)

        context = {
            'search_form': search_form,
            'filters_form': filters_form,
            'sort_form': sort_form,
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


class NewsApiSources(NewsApiBaseView):
    template_name = 'news/sources_list.html'

    def get(self, request, *_args, **_kwargs):
        filters_form = news.forms.SourcesFilterForm(request.GET)

        if not filters_form.is_valid():
            django.contrib.messages.error(request, _('Forms_error'))
            context = {
                'filters_form': filters_form,
                'sources': [],
            }
            return django.shortcuts.render(request, self.template_name, context)

        params = {
            'country': ','.join(filters_form.cleaned_data.get('country')),
            'category': ','.join(filters_form.cleaned_data.get('category')),
            'language': ','.join(filters_form.cleaned_data.get('language')),
        }

        response = api.newsApi.NewsApi().get_sources_list(params=params)

        sources_list = response.get('sources', [])

        context = {
            'filters_form': filters_form,
            'sources': sources_list,
        }

        return django.shortcuts.render(
            request,
            self.template_name,
            context,
        )


class FavoritesView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.ListView):
    model = news.models.FavoriteArticle
    template_name = 'users/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news'] = [
            {
                'title': fav.title,
                'description': fav.description,
                'content': fav.content,
                'url': fav.url,
                'urlToImage': fav.url_to_image,
                'author': fav.author,
                'source': fav.source,
                'publishedAt': fav.published_at,
                'is_favorite': True,
            }
            for fav in context.get('favorites', [])
        ]

        return context


class SaveFavoriteView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.View):
    def post(self, request, *_args, **_kwargs):
        data = request.POST

        url = data.get('url')

        if not url:
            return django.http.JsonResponse(
                {'error': 'URL is required'},
                status=HTTPStatus.BAD_REQUEST,
            )

        favorite, created = news.models.FavoriteArticle.objects.get_or_create(
            user=request.user,
            url=url,
            defaults={
                'title': data.get('title'),
                'description': data.get('description'),
                'content': data.get('content'),
                'url_to_image': data.get('url_to_image'),
                'source': data.get('source'),
                'author': data.get('author'),
                'published_at': data.get('published_at'),
                'category': data.get('category'),
            },
        )

        if not created:
            favorite.delete()
            return django.http.JsonResponse({'status': 'removed'}, status=HTTPStatus.OK)

        return django.http.JsonResponse({'status': 'added'}, status=HTTPStatus.CREATED)
