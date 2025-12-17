__all__ = ('ProfileView', 'SignUpView', 'FavoritesView', 'SaveFavoriteView')

from http import HTTPStatus

import django.contrib
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.messages
import django.core.exceptions
import django.db
import django.http
import django.shortcuts
import django.urls
import django.utils
import django.utils.dateparse
import django.utils.timezone
import django.views.generic

import users.forms
import users.models


class SignUpView(django.views.generic.CreateView):
    form_class = users.forms.SignupForm
    template_name = 'users/signup.html'
    success_url = django.urls.reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        django.contrib.auth.login(self.request, user)

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
    form_class = users.forms.ProfileForm
    success_url = django.urls.reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        profile, created = users.models.Profile.objects.get_or_create(user=self.request.user)
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


class FavoritesView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.generic.ListView):
    model = users.models.FavoriteArticle
    template_name = 'users/favorites.html'
    context_object_name = 'favorites'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['news'] = [
            {
                'title': fav.title,
                'description': fav.description,
                'content': fav.content,
                'url': fav.url,
                'image_url': fav.image_url,
                'creator': fav.creator,
                'author': fav.creator,
                'source': fav.source_name,
                'publishedAt': fav.published_at,
                'id': fav.article_id,
                'is_favorite': True,
                'favorited_at': fav.created_at,
            }
            for fav in context.get('favorites', [])
        ]

        return context


class SaveFavoriteView(django.contrib.auth.mixins.LoginRequiredMixin, django.views.View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        article_id = data.get('article_id')
        if not article_id:
            return django.http.JsonResponse(
                {'error': 'article_id is required'},
                status=HTTPStatus.BAD_REQUEST,
            )

        try:
            published_at_str = data.get('published_at', '').strip()
            if published_at_str:
                dt = django.utils.dateparse.parse_datetime(published_at_str)
                if dt and not django.utils.timezone.is_aware(dt):
                    dt = django.utils.timezone.make_aware(dt, django.utils.timezone.utc)
            else:
                dt = django.utils.timezone.now()

            obj, created = users.models.FavoriteArticle.objects.get_or_create(
                user=request.user,
                article_id=article_id,
                defaults={
                    'user': request.user,
                    'article_id': article_id,
                    'title': data['title'][:499],
                    'description': data.get('description', ''),
                    'content': data.get('content', ''),
                    'url': data['url'],
                    'image_url': data.get('image_url', ''),
                    'source_name': data.get('source_name', ''),
                    'source_id': data.get('source_id', ''),
                    'creator': data.get('creator', ''),
                    'published_at': dt,
                    'category': data.get('category', ''),
                    'tags': [],
                },
            )

            if not created:
                obj.delete()
                return django.http.JsonResponse({'status': 'removed'})

            return django.http.JsonResponse({'status': 'added'})

        except django.db.IntegrityError:
            return django.http.JsonResponse({'status': 'removed'})
        except Exception as e:
            return django.http.JsonResponse({'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
