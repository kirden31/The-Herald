__all__ = ('create_save_user_profile',)

import django.db.models.signals
import django.dispatch

import users.models


@django.dispatch.receiver(
    django.db.models.signals.post_save,
    sender=users.models.User,
)
def create_save_user_profile(sender, instance, created, **_kwargs):
    if created:
        users.models.Profile.objects.create(user=instance)
    else:
        users.models.Profile.objects.update_or_create(user=instance)
