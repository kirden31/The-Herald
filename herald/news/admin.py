__all__ = ('FavoriteArticleAdmin',)

import django.contrib
from django.utils.translation import gettext_lazy as _

import news.models


@django.contrib.admin.register(news.models.FavoriteArticle)
class FavoriteArticleAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        news.models.FavoriteArticle.user.field.name,
        news.models.FavoriteArticle.title.field.name,
        news.models.FavoriteArticle.published_at.field.name,
        'get_source_preview',
    )
    list_filter = (
        news.models.FavoriteArticle.user.field.name,
        news.models.FavoriteArticle.published_at.field.name,
    )
    search_fields = (
        news.models.FavoriteArticle.title.field.name,
        news.models.FavoriteArticle.description.field.name,
        news.models.FavoriteArticle.user.field.name,
        news.models.FavoriteArticle.source.field.name,
        news.models.FavoriteArticle.author.field.name,
    )
    ordering = (news.models.FavoriteArticle.published_at.field.name,)
    readonly_fields = (
        news.models.FavoriteArticle.title.field.name,
        news.models.FavoriteArticle.description.field.name,
        news.models.FavoriteArticle.user.field.name,
        news.models.FavoriteArticle.source.field.name,
        news.models.FavoriteArticle.author.field.name,
        news.models.FavoriteArticle.published_at.field.name,
        news.models.FavoriteArticle.url.field.name,
        news.models.FavoriteArticle.url_to_image.field.name,
    )

    fieldsets = (
        (
            _('Пользователь и источник'),
            {
                'fields': (
                    news.models.FavoriteArticle.user.field.name,
                    news.models.FavoriteArticle.source.field.name,
                    news.models.FavoriteArticle.author.field.name,
                ),
            },
        ),
        (
            _('Содержание новости'),
            {
                'fields': (
                    news.models.FavoriteArticle.title.field.name,
                    news.models.FavoriteArticle.description.field.name,
                ),
            },
        ),
        (
            _('Ссылки и дата'),
            {
                'fields': (
                    news.models.FavoriteArticle.url.field.name,
                    news.models.FavoriteArticle.url_to_image.field.name,
                    news.models.FavoriteArticle.published_at.field.name,
                ),
            },
        ),
    )

    @django.contrib.admin.display(description=_('Источник'))
    def get_source_preview(self, obj):
        return obj.source[:50] + '...' if obj.source and len(obj.source) > 50 else obj.source
