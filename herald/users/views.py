__all__ = ()

import datetime

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from users.forms import SignupForm
from users.models import FavoriteArticle


class SignUpView(CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(self.request, user)

        messages.success(self.request, 'Регистрация прошла успешно! Добро пожаловать!')

        return response

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile if hasattr(self.request.user, 'profile') else None
        return context


class FavoritesView(LoginRequiredMixin, ListView):
    model = FavoriteArticle
    template_name = 'users/favorites.html'
    context_object_name = 'favorites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        week_qs = FavoriteArticle.objects.filter(
            user=user,
            created_at__gte=week_ago,
        )
        context['this_week_count'] = week_qs.count()
        categories_qs = FavoriteArticle.objects.filter(user=user)
        categories_qs = categories_qs.exclude(category__isnull=True)
        context['categories_count'] = (
            categories_qs.values(
                'category',
            )
            .distinct()
            .count()
        )
        sources_qs = FavoriteArticle.objects.filter(user=user)
        context['sources_count'] = (
            sources_qs.values(
                'source_name',
            )
            .distinct()
            .count()
        )
        all_cats_qs = FavoriteArticle.objects.filter(user=user)
        all_cats_qs = all_cats_qs.exclude(category__isnull=True)
        context['all_categories'] = all_cats_qs.values_list(
            'category',
            flat=True,
        ).distinct()

        return context
