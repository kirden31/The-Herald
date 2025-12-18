__all__ = ()

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy
from users.models import Profile, User


class ConfigAuthBackend(ModelBackend):
    def _email_detector(self, login_item):
        try:
            validate_email(login_item)
            return True
        except ValidationError:
            return False

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        is_email = self._email_detector(username)

        if is_email:
            try:
                user = User.objects.by_mail(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user is None:
            return None

        if not hasattr(user, 'profile'):
            try:
                Profile.objects.create(user=user)
            except Exception:
                return None

        if user.check_password(password) and self.user_can_authenticate(
            user=user,
        ):
            user.profile.attempts_count = 0
            user.profile.save()
            return user

        user.profile.attempts_count += 1

        if user.profile.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
            user.is_active = False
            user.profile.block_date = timezone.now()
            user.save()

            self._add_message_safe(
                request,
                gettext_lazy(
                    'The maximum number of attempts has been reached.',
                ),
            )

            if request:
                activation_url = request.build_absolute_uri(
                    reverse('users:reactivate', kwargs={'pk': user.id}),
                )

                msg = gettext_lazy(
                    'We have noticed suspicious activity,'
                    'That s why your account was blocked.'
                    'Follow the activation link (valid for 7 days):',
                )
                send_mail(
                    subject=gettext_lazy('Account activation.'),
                    message=f'{msg} {activation_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

        attempts_left = settings.MAX_AUTH_ATTEMPTS - user.profile.attempts_count
        self._add_message_safe(
            request,
            f"{gettext_lazy('You have attempts remaining:')} {attempts_left}",
        )

        user.profile.save()
        return None

    def _add_message_safe(self, request, message):
        try:
            if request and hasattr(request, '_messages'):
                messages.error(request, message)
        except Exception:
            pass
