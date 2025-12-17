from django.contrib.auth import views
import django.urls

import users.forms
import users.views

app_name = 'users'
urlpatterns = [
    django.urls.path('signup/', users.views.SignUpView.as_view(), name='signup'),
    django.urls.path('profile/', users.views.ProfileView.as_view(), name='profile'),
    django.urls.path('favorites/', users.views.FavoritesView.as_view(), name='favorites'),
    django.urls.path(
        'save-favorite/',
        users.views.SaveFavoriteView.as_view(),
        name='save_favorite',
    ),
    django.urls.path(
        'login/',
        views.LoginView.as_view(
            form_class=users.forms.LoginForm,
            template_name='users/login.html',
        ),
        name='login',
    ),
    django.urls.path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logout.html'),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset',
        views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
