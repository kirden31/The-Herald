__all__ = ('FavoriteArticle',)


import django.db
from django.utils.translation import gettext_lazy as _

import users.models


class FavoriteArticle(django.db.models.Model):
    user = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='favorite_articles',
        verbose_name=_('пользователь'),
    )
    title = django.db.models.CharField(verbose_name=_('заголовок'))
    description = django.db.models.TextField(verbose_name=_('описание'), blank=True, null=True)
    content = django.db.models.TextField(verbose_name=_('содержание'), blank=True, null=True)
    url = django.db.models.URLField(verbose_name=_('ссылка на новость'))
    urlToImage = django.db.models.URLField(  # noqa: N815
        verbose_name=_('ссылка на изображение'),
        blank=True,
        null=True,
    )
    source = django.db.models.CharField(verbose_name=_('название источника'))
    author = django.db.models.CharField(verbose_name=_('автор'), blank=True, null=True)
    publishedAt = django.db.models.DateTimeField(verbose_name=_('дата публикации'))  # noqa: N815
    category = django.db.models.CharField(verbose_name=_('категория'), blank=True, null=True)

    class Meta:
        verbose_name = _('избранная новость')
        verbose_name_plural = _('избранные новости')
        unique_together = ['user', 'url']
        ordering = ['-publishedAt']
        indexes = [
            django.db.models.Index(fields=['user', 'publishedAt']),
            django.db.models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.user.username[:10]} - {self.title[:50]}'

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'urlToImage': self.urlToImage,
            'source': self.source,
            'author': self.author,
            'publishedAt': self.publishedAt.isoformat(),
            'category': self.category,
            'is_favorite': True,
        }
