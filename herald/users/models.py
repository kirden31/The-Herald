__all__ = ('User', 'Profile', 'FavoriteArticle')

import sys

import django.conf
import django.contrib.auth.models
import django.db
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate']):
    django.contrib.auth.models.User._meta.get_field('email')._unique = True


class UserManager(django.contrib.auth.models.BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def active(self):
        return self.get_queryset().filter(is_active=True)


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = django.contrib.auth.models.User._meta.verbose_name
        verbose_name_plural = django.contrib.auth.models.User._meta.verbose_name_plural

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username[:10]


class Profile(django.db.models.Model):
    def image_path(self, filename):
        return f'users/avatars/{self.user.id}/{filename}'

    user = django.db.models.OneToOneField(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
        related_name='profile',
        verbose_name=_('пользователь'),
    )
    image = django.db.models.ImageField(
        upload_to=image_path,
        blank=True,
        verbose_name=_('аватарка'),
        help_text=_('Аватарка пользователя.'),
    )
    birthday = django.db.models.DateField(
        blank=True,
        null=True,
        verbose_name=_('дата рождения'),
        help_text=_('Дата рождения пользователя.'),
    )
    location = django.db.models.CharField(
        blank=True,
        help_text=_('Город (или страна) проживания пользователя.'),
    )
    attempts_count = django.db.models.PositiveBigIntegerField(
        default=0,
        verbose_name=_('попытки'),
        help_text=_('Количество попыток входа в систему'),
    )

    def get_image_300x300(self):
        if self.image:
            return sorl.thumbnail.get_thumbnail(
                self.image,
                '300x300',
                crop='center',
                quality=51,
            )

        return None

    class Meta:
        verbose_name = _('профиль')
        verbose_name_plural = _('профили')

    def __str__(self):
        return self.user.username[:10]


class FavoriteArticle(django.db.models.Model):
    user = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        related_name='favorite_articles',
        verbose_name=_('пользователь'),
    )
    article_id = django.db.models.CharField(verbose_name=_('id новости'), db_index=True)
    title = django.db.models.CharField(verbose_name=_('заголовок'))
    description = django.db.models.TextField(verbose_name=_('описание'), blank=True, null=True)
    content = django.db.models.TextField(verbose_name=_('содержание'), blank=True, null=True)
    url = django.db.models.URLField(verbose_name=_('ссылка на новость'))
    image_url = django.db.models.URLField(
        verbose_name=_('ссылка на изображение'),
        blank=True,
        null=True,
    )
    source_name = django.db.models.CharField(verbose_name=_('название источника'))
    source_id = django.db.models.CharField(verbose_name=_('id источника'), blank=True, null=True)
    creator = django.db.models.CharField(verbose_name=_('автор'), blank=True, null=True)
    published_at = django.db.models.DateTimeField(verbose_name=_('дата публикации'))
    category = django.db.models.CharField(verbose_name=_('категория'), blank=True, null=True)
    created_at = django.db.models.DateTimeField(
        verbose_name=_('дата добавления'),
        auto_now_add=True,
    )
    tags = django.db.models.JSONField(
        verbose_name=_('теги'),
        default=list,
        help_text=_('Теги для поиска и фильтрации'),
    )

    class Meta:
        verbose_name = _('избранная новость')
        verbose_name_plural = _('избранные новости')
        unique_together = ['user', 'article_id']
        ordering = ['-created_at']
        indexes = [
            django.db.models.Index(fields=['user', 'created_at']),
            django.db.models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.user.username[:10]} - {self.title[:50]}'

    def to_dict(self):
        return {
            'id': self.article_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'image_url': self.image_url,
            'source': self.source_name,
            'creator': self.creator,
            'published_at': self.published_at.isoformat(),
            'category': self.category,
            'is_favorite': True,
            'favorited_at': self.created_at.isoformat(),
        }
