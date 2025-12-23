__all__ = ('ProfileView', 'ProfileUpdateView', 'SignUpView')

import datetime

import django.contrib
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.messages
import django.shortcuts
import django.urls
from django.utils.translation import gettext as _
import django.views.generic

import users.forms
import users.models

ACTIVATE_LINK_VALID_HOURS = 12
REACTIVATE_LINK_VALID_HOURS = 7 * 24


class AccountActivateView(django.views.View):
    template_name = 'users/account_activate.html'
    model = users.models.User
    time_delta = ACTIVATE_LINK_VALID_HOURS

    def get(self, request, pk, *args, **kwargs):
        user = django.shortcuts.get_object_or_404(
            users.models.User,
            pk=pk,
        )

        if user.is_active:
            context = {'mes': _('Already_activated'), 'user': user}
        else:
            context = self.account_action(user)

        return django.shortcuts.render(request, self.template_name, context)

    def check_delta(self, dt):
        now = django.utils.timezone.now()
        delta = now - dt

        if delta <= datetime.timedelta(hours=self.time_delta):
            return True

        return False

    def account_action(self, user):
        if self.check_delta(user.date_joined):
            user.is_active = True
            user.save()
            return {'mes': _('Activation_successful'), 'user': user}

        return {'mes': _('Activation_time_expired'), 'user': user}


class AccountReactivateView(AccountActivateView):
    time_delta = REACTIVATE_LINK_VALID_HOURS

    def account_action(self, user):
        if user.profile.blocked_at:
            if self.check_delta(user.profile.blocked_at):
                user.is_active = True
                user.profile.blocked_at = None
                user.save()
                return {'mes': _('Activation_successful'), 'user': user}

            return {'mes': _('Activation_time_expired'), 'user': user}

        return {'mes': _('Account_is_not_deactivated'), 'user': user}


class SignUpView(django.views.generic.CreateView):
    form_class = users.forms.SignupForm
    template_name = 'users/signup.html'
    success_url = django.urls.reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)

        django.contrib.auth.login(self.request, self.object)

        django.contrib.messages.success(
            self.request,
            _('Registration_successful_Welcome'),
        )

        return response

    def get(self, request, *args, **kwargs):
        if request.user:
            return django.shortcuts.redirect('/')

        return super().get(request, *args, **kwargs)


class ProfileView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.TemplateView):
    template_name = 'users/profile.html'


class ProfileUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    template_name = 'users/profile_update.html'
    model = users.models.Profile
    form_class = users.forms.ProfileForm
    success_url = django.urls.reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        profile, _ = users.models.Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        django.contrib.messages.success(
            self.request,
            _('Profile_successfully_updated'),
        )
        return response
