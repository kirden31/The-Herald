__all__ = ('UserAdmin',)

import django.contrib
import django.contrib.auth.admin
from django.utils.translation import gettext_lazy as _

import users.models


class ProfileInline(django.contrib.admin.StackedInline):
    model = users.models.Profile
    can_delete = False
    verbose_name_plural = _('Профиль')
    fk_name = 'user'

    fields = (
        users.models.Profile.image.field.name,
        users.models.Profile.birthday.field.name,
        users.models.Profile.location.field.name,
        users.models.Profile.favorite_categories.field.name,
        users.models.Profile.attempts_count.field.name,
    )
    readonly_fields = (users.models.Profile.attempts_count.field.name,)


@django.contrib.admin.register(users.models.User)
class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)

    list_display = (
        users.models.User.username.field.name,
        users.models.User.email.field.name,
        users.models.User.first_name.field.name,
        users.models.User.last_name.field.name,
        users.models.User.is_staff.field.name,
        users.models.User.is_active.field.name,
        users.models.User.date_joined.field.name,
    )
    list_filter = (
        users.models.User.is_staff.field.name,
        users.models.User.is_superuser.field.name,
        users.models.User.is_active.field.name,
        users.models.User.date_joined.field.name,
    )
    search_fields = (
        users.models.User.username.field.name,
        users.models.User.email.field.name,
        users.models.User.first_name.field.name,
        users.models.User.last_name.field.name,
    )
    ordering = (users.models.User.date_joined.field.name,)
    readonly_fields = (
        users.models.User.date_joined.field.name,
        users.models.User.last_login.field.name,
    )
