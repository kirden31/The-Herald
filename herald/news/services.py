__all__ = ('enrich_with_favorites',)

import news.models


def enrich_with_favorites(news_list, user):
    article_urls = [a['url'] for a in news_list if a.get('url')]
    if not article_urls:
        return news_list

    favorite_urls = news.models.FavoriteArticle.objects.filter(
        user=user,
        url__in=article_urls,
    ).values_list('url', flat=True)

    for article in news_list:
        url = article.get('url')
        article['is_favorite'] = url in favorite_urls

    return news_list
