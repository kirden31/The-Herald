__all__ = ('ProfileView', 'ProfileUpdateView', 'SignUpView')

import django.contrib
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.messages
import django.shortcuts
import django.urls
import django.views.generic

import users.forms
import users.models


class SignUpView(django.views.generic.CreateView):
    form_class = users.forms.SignupForm
    template_name = 'users/signup.html'
    success_url = django.urls.reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)

        django.contrib.auth.login(self.request, self.object)

        django.contrib.messages.success(
            self.request,
            'Регистрация прошла успешно! Добро пожаловать!',
        )

        return response

    def get(self, request, *args, **kwargs):
        if request.user:
            return django.shortcuts.redirect('/')

        return super().get(request, *args, **kwargs)


class ProfileView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['favorite_count'] = user.favorite_articles.count()
        return context


class ProfileUpdateView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.UpdateView,
):
    template_name = 'users/profile_update.html'
    model = users.models.User
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
            'Профиль успешно обновлен!',
        )
        return response
