__all__ = ('create_save_user_profile',)

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Profile


@receiver(post_save, sender=User)
def create_save_user_profile(sender, instance, created, **_kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.update_or_create(user=instance)
