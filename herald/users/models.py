__all__ = ('User', 'Profile')

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
