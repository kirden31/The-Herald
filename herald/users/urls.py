from django.contrib.auth import views
from django.urls import path

import users.forms
import users.views

app_name = 'users'
urlpatterns = [
    path(
        'activate/<str:username>',
        users.views.AccountActivateView.as_view(),
        name='account_activate',
    ),
    path(
        'reactivate/<int:pk>',
        users.views.AccountReactivateView.as_view(),
        name='account_reactivate',
    ),
    path('signup/', users.views.SignUpView.as_view(), name='signup'),
    path('profile/', users.views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', users.views.ProfileUpdateView.as_view(), name='profile_edit'),
    path(
        'login/',
        views.LoginView.as_view(
            form_class=users.forms.LoginForm,
            template_name='users/login.html',
        ),
        name='login',
    ),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='users/logout.html'),
        name='logout',
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset',
        views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
        ),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
