__all__ = ('FavoriteArticleAdmin',)

import django.contrib.admin
from django.utils.translation import gettext_lazy as _

from news.models import FavoriteArticle


@django.contrib.admin.register(FavoriteArticle)
class FavoriteArticleAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        FavoriteArticle.user.field.name,
        FavoriteArticle.title.field.name,
        FavoriteArticle.published_at.field.name,
        'get_source_preview',
    )
    list_filter = (
        FavoriteArticle.user.field.name,
        FavoriteArticle.published_at.field.name,
    )
    search_fields = (
        FavoriteArticle.title.field.name,
        FavoriteArticle.description.field.name,
        FavoriteArticle.user.field.name,
        FavoriteArticle.source.field.name,
        FavoriteArticle.author.field.name,
    )
    ordering = (FavoriteArticle.published_at.field.name,)
    readonly_fields = (
        FavoriteArticle.title.field.name,
        FavoriteArticle.description.field.name,
        FavoriteArticle.user.field.name,
        FavoriteArticle.source.field.name,
        FavoriteArticle.author.field.name,
        FavoriteArticle.published_at.field.name,
        FavoriteArticle.url.field.name,
        FavoriteArticle.url_to_image.field.name,
    )

    user_and_source = (
        FavoriteArticle.user.field.name,
        FavoriteArticle.source.field.name,
        FavoriteArticle.author.field.name,
    )

    news_content = (
        FavoriteArticle.title.field.name,
        FavoriteArticle.description.field.name,
    )

    link_and_date = (
        FavoriteArticle.url.field.name,
        FavoriteArticle.url_to_image.field.name,
        FavoriteArticle.published_at.field.name,
    )

    fieldsets = (
        (
            _('User_and_source'),
            {
                'fields': user_and_source,
            },
        ),
        (
            _('News_content'),
            {
                'fields': news_content,
            },
        ),
        (
            _('Link_and_date'),
            {
                'fields': link_and_date,
            },
        ),
    )

    @django.contrib.admin.display(description=_('Source'))
    def get_source_preview(self, obj):
        return obj.source[:50] + '...' if obj.source and len(obj.source) > 50 else obj.source
