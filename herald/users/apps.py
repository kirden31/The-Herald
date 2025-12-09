__all__ = ()

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _('Пользователи')

    def ready(self):
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save

        from users.signals import create_profile, save_profile

        post_save.connect(create_profile, sender=User)
        post_save.connect(save_profile, sender=User)
