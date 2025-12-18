from django.urls import path

import news.views

app_name = 'news'

urlpatterns = (
    path(
        'save_favorite/',
        news.views.SaveFavoriteView.as_view(),
        name='save_favorite',
    ),
    path(
        'favorite/',
        news.views.FavoritesView.as_view(),
        name='favorite',
    ),
    path(
        'everything-news/',
        news.views.EverythingNews.as_view(),
        name='everything_news',
    ),
    path(
        'top-headlines-news/',
        news.views.TopHeadlinesNews.as_view(),
        name='top_headlines_news',
    ),
    path(
        'top-headlines-sources/',
        news.views.TopHeadlinesSource.as_view(),
        name='top_headlines_sources',
    ),
    path(
        'guardian-news/',
        news.views.GuardianNews.as_view(),
        name='guardian_news',
    ),
)
