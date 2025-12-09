__all__ = ()

import sys

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, User
from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import get_thumbnail

if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate']):
    User._meta.get_field('email')._unique = True


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def active(self):
        return self.get_queryset().filter(is_active=True)


class User(User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = User._meta.verbose_name
        verbose_name_plural = User._meta.verbose_name_plural

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username[:10]


class Profile(models.Model):
    def image_path(self, filename):
        return f'users/avatars/{self.user.id}/{filename}'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('пользователь'),
    )
    image = models.ImageField(
        upload_to=image_path,
        blank=True,
        verbose_name=_('аватарка'),
        help_text=_('Аватарка пользователя.'),
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('дата рождения'),
        help_text=_('Дата рождения пользователя.'),
    )
    location = models.CharField(
        blank=True,
        help_text=_('Город (или страна) проживания пользователя.'),
    )
    attempts_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=_('попытки'),
        help_text=_('Количество попыток входа в систему'),
    )

    def get_image_300x300(self):
        if self.image:
            return get_thumbnail(
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


class FavoriteArticle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_articles',
        verbose_name=_('пользователь'),
    )
    article_id = models.CharField(
        'ID новости',
        max_length=500,
        db_index=True,
    )
    title = models.CharField(
        verbose_name=_('заголовок'),
        max_length=500,
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    content = models.TextField(
        'Содержание',
        blank=True,
        null=True,
    )
    url = models.URLField(
        'Ссылка на новость',
        max_length=500,
    )
    image_url = models.URLField(
        'Ссылка на изображение',
        max_length=500,
        blank=True,
        null=True,
    )
    source_name = models.CharField(
        'Название источника',
        max_length=200,
    )
    source_id = models.CharField(
        'ID источника',
        max_length=100,
        blank=True,
        null=True,
    )
    creator = models.CharField(
        'Автор',
        max_length=200,
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField('Дата публикации')
    category = models.CharField('Категория', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    tags = models.JSONField('Теги', default=list, help_text='Теги для поиска и фильтрации')

    class Meta:
        verbose_name = 'Избранная новость'
        verbose_name_plural = 'Избранные новости'
        unique_together = ['user', 'article_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'category']),
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
