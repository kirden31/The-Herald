__all__ = ('enrich_with_favorites',)

import news.models


def enrich_with_favorites(news_list, user):
    if not user:
        return news_list

    article_urls = [a['url'] for a in news_list if a.get('url')]
    if not article_urls:
        return news_list

    queryset = news.models.FavoriteArticle.objects.filter(
        user=user,
        url__in=article_urls,
    )
    favorite_urls = set(queryset.values_list('url', flat=True))

    for article in news_list:
        url = article.get('url')
        if url:
            article['is_favorite'] = url in favorite_urls
        else:
            article['is_favorite'] = False

    return news_list
