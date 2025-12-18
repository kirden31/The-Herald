__all__ = ('ConfigAuthBackend',)

import django.conf
import django.contrib
import django.contrib.auth.backends
import django.core.exceptions
import django.core.mail
import django.core.validators
import django.urls
import django.utils
from django.utils.translation import gettext_lazy

import users.models


class ConfigAuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            try:
                django.core.validators.validate_email(username)
                user = users.models.User.objects.get(email=username)
            except django.core.exceptions.ValidationError:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(
            user=user,
        ):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1

        if user.profile.attempts_count > django.conf.settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.profile.block_date = django.utils.timezone.now()

            if request:
                activation_url = request.build_absolute_uri(
                    django.urls.reverse('users:reactivate', kwargs={'pk': user.id}),
                )

                msg = gettext_lazy(
                    'We have noticed suspicious activity,'
                    'That s why your account was blocked.'
                    'Follow the activation link (valid for 7 days):',
                )
                django.core.mail.send_mail(
                    subject=gettext_lazy('Account activation.'),
                    message=f'{msg} {activation_url}',
                    from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

        user.save()
        return None

    def get_user(self, user_id):
        try:
            return users.models.User.objects.get(pk=user_id)
        except users.models.User.DoesNotExist:
            return None
