__all__ = ('ConfigAuthBackend',)

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy

from users.models import User


class ConfigAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            try:
                validate_email(username)
                user = User.objects.get(email=username)
            except ValidationError:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(
            user=user,
        ):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1

        if user.profile.attempts_count > settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.profile.block_date = timezone.now()

            self._add_message_safe(
                request,
                gettext_lazy(
                    'Достигнуто максимальное количество попыток.',
                ),
            )

            if request:
                activation_url = request.build_absolute_uri(
                    reverse('users:reactivate', kwargs={'pk': user.id}),
                )

                msg = gettext_lazy(
                    'Мы заметили подозрительную активность, '
                    'поэтому заблокировали ваш аккаунт.'
                    'Перейдите по ссылке для активации (действует 7 дней):',
                )
                send_mail(
                    subject=gettext_lazy('Активация аккаунта.'),
                    message=f'{msg} {activation_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

        attempts_left = settings.MAX_AUTH_ATTEMPTS - user.profile.attempts_count
        self._add_message_safe(
            request,
            f"{gettext_lazy('У вас осталось попыток:')} {attempts_left}",
        )

        user.save()
        return None

    def _add_message_safe(self, request, message):
        try:
            if request and hasattr(request, '_messages'):
                messages.error(request, message)
        except Exception:
            pass
