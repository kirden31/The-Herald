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

    def by_mail(self, email):
        if not email:
            return None

        return self.get_queryset().filter(email=email).first()


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
        return self.username


class Profile(models.Model):
    def image_path(self, filename):
        return f'users/avatars/{self.user.id}/{filename}'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('user'),
    )
    image = models.ImageField(
        upload_to=image_path,
        blank=True,
        verbose_name=_('avatar'),
        help_text=_('User avatar.'),
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('date of birth'),
        help_text=_('User date of birth.'),
    )
    location = models.CharField(
        blank=True,
        help_text=_('The user city (or country) of residence.'),
    )
    attempts_count = models.PositiveBigIntegerField(
        default=0,
        verbose_name=_('attempts'),
        help_text=_('Number of login attempts'),
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
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.user.username


class FavoriteArticle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_articles',
        verbose_name=_('user'),
    )
    article_id = models.CharField(
        _('ID_News'),
        max_length=500,
        db_index=True,
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=500,
    )
    description = models.TextField(
        _('Description'),
        blank=True,
        null=True,
    )
    content = models.TextField(
        _('Content'),
        blank=True,
        null=True,
    )
    url = models.URLField(
        _('Link to news'),
        max_length=500,
    )
    image_url = models.URLField(
        _('Image link'),
        max_length=500,
        blank=True,
        null=True,
    )
    source_name = models.CharField(_('Source name'), max_length=200)
    source_id = models.CharField(
        _('ID_Source'),
        max_length=100,
        blank=True,
        null=True,
    )
    creator = models.CharField(
        _('Author'),
        max_length=200,
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(_('Publication date'))
    category = models.CharField(_('Category'), max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(_('Date added'), auto_now_add=True)
    tags = models.JSONField(_('Tags'), default=list, help_text=_('Tags for searching and filtering'))

    class Meta:
        verbose_name = _('Featured news')
        verbose_name_plural = _('Featured News')
        unique_together = ['user', 'article_id']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['user', 'category']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.title[:50]}'

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
