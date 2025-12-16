__all__ = ('add_article_id_and_source', 'enrich_with_favorites')

import users.models


def add_article_id_and_source(news_list, source_type='newsapi'):
    for article in news_list:
        article['id'] = (article.get('url') or '').strip() or f'unknown_{hash(str(article))}'
        if source_type == 'newsapi':
            article['source_name'] = article.get('source', 'NewsAPI')
            article['source_id'] = ''
            article['image_url'] = article.get('urlToImage', '').strip()
        elif source_type == 'guardian':
            article['source_name'] = 'The Guardian'
            article['source_id'] = 'guardian'
            article['image_url'] = ''
        else:
            article['source_name'] = 'Unknown'
            article['source_id'] = ''
            article['image_url'] = ''

        article['creator'] = article.get('author', '')
        article['is_favorite'] = False

    return news_list


def enrich_with_favorites(news_list, user):
    if not user.is_authenticated:
        return news_list

    article_ids = [a['id'] for a in news_list if a.get('id')]
    if not article_ids:
        return news_list

    queryset = users.models.FavoriteArticle.objects.filter(
        user=user,
        article_id__in=article_ids,
    )
    favorite_ids = set(queryset.values_list('article_id', flat=True))

    for article in news_list:
        article['is_favorite'] = article['id'] in favorite_ids

    return news_list
