__all__ = ('UsersConfig',)

import django.apps
from django.utils.translation import gettext_lazy as _


class UsersConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _('Пользователи')

    def ready(self):
        import django.contrib.auth.models
        import django.db.models.signals

        import users.signals

        django.db.models.signals.post_save.connect(
            users.signals.create_profile,
            sender=django.contrib.auth.models.User,
        )
        django.db.models.signals.post_save.connect(
            users.signals.save_profile,
            sender=django.contrib.auth.models.User,
        )
