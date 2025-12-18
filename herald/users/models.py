__all__ = ('User', 'Profile')

import sys

import django.conf
import django.contrib.auth.models
import django.db
import django.db.models
from django.utils.translation import gettext_lazy as _
import sorl.thumbnail

import users.validators


class UserManager(django.contrib.auth.models.BaseUserManager):
    EMAIL_DOMAIN_CANONICAL_FORM = {
        'ya.ru': 'yandex.ru',
    }
    DOTS_CANONICAL_FORM = {
        'yandex.ru': '-',
        'gmail.com': '',
    }

    def get_queryset(self):
        return super().get_queryset().select_related('profile')

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def normalize_email(self, email):
        email = super().normalize_email(email)

        if not email:
            return email

        local, domain = email.lower().split('@')

        domain = self.EMAIL_DOMAIN_CANONICAL_FORM.get(domain, domain)

        local = local.replace('.', self.DOTS_CANONICAL_FORM.get(domain, ''))

        local = local.split('+')[0]
        return f'{local}@{domain}'


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
        return self.username[:15]


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
        null=True,
        verbose_name=_('аватарка'),
        help_text=_('Аватарка пользователя.'),
    )
    birthday = django.db.models.DateField(
        blank=True,
        null=True,
        validators=[users.validators.ValidateBirthdayDate()],
        verbose_name=_('дата рождения'),
        help_text=_('Дата рождения пользователя.'),
    )
    location = django.db.models.CharField(
        blank=True,
        null=True,
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
        return self.user.username[:15]


if not any(arg in ('makemigrations', 'migrate') for arg in sys.argv):
    User._meta.get_field('email')._unique = True
