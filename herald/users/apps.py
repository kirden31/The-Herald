__all__ = ('UsersConfig',)

import django.apps
from django.utils.translation import gettext_lazy as _


class UsersConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _('Пользователи')

    def ready(self):
        import users.signals  # noqa
