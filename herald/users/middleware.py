__all__ = ('CustomRequestUser', 'get_user')

import django.contrib.auth
import django.utils.functional

import users.models


class CustomRequestUser:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        request.user = django.utils.functional.SimpleLazyObject(
            lambda: get_user(user),
        )

        return self.get_response(request)


def get_user(user):
    if isinstance(user, django.contrib.auth.models.AnonymousUser):
        return None

    if isinstance(user, users.models.User):
        return user

    return users.models.User.objects.get(pk=user.pk)
