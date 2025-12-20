__all__ = ('FavoriteArticle',)


import django.db.models
from django.utils.translation import gettext_lazy as _

import users.models


class FavoriteArticle(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='favorite_articles',
        verbose_name=_('user'),
    )

    title = django.db.models.CharField(
        verbose_name=_('title'),
        null=True,
    )
    description = django.db.models.TextField(verbose_name=_('description'), null=True)
    content = django.db.models.TextField(
        verbose_name=_('content'),
        null=True,
    )
    url = django.db.models.URLField(
        verbose_name=_('link_to_news'),
    )
    url_to_image = django.db.models.URLField(
        verbose_name=_('image_link'),
        null=True,
    )
    source = django.db.models.CharField(
        verbose_name=_('source_name'),
        null=True,
    )
    author = django.db.models.CharField(
        verbose_name=_('author'),
        null=True,
    )
    published_at = django.db.models.DateTimeField(
        verbose_name=_('publication_date'),
        null=True,
    )
    category = django.db.models.CharField(
        verbose_name=_('category'),
        null=True,
    )

    class Meta:
        verbose_name = _('featured_news')
        verbose_name_plural = _('selected_news')
        unique_together = ['user', 'url']
        ordering = ['-published_at']
        indexes = [
            django.db.models.Index(fields=['user', 'published_at']),
            django.db.models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.user.username[:10]} - {self.title[:50]}'

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'urlToImage': self.url_to_image,
            'source': self.source,
            'author': self.author,
            'publishedAt': self.published_at.isoformat(),
            'category': self.category,
            'is_favorite': True,
        }
