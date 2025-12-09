__all__ = ()

import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from users.models import Profile

User = get_user_model()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class SignupForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label=_('Почта'),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        exclude = (User.first_name.field.name,)
        fields = UserCreationForm.Meta.fields + (User.email.field.name,)
        labels = {
            User.username.field.name: _('Логин'),
            User.email.field.name: _('Почта'),
        }
        help_text = {
            User.username.field.name: _('Введите логин'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _('Пользователь с таким email уже существует.'),
                code='duplicate_code',
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()

        return user


class ChangeForm(BootstrapFormMixin, UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = UserChangeForm.Meta.fields


class UserForm(BootstrapFormMixin, ModelForm):
    class Meta:
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        )


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields[User.email.field.name].initial = self.user.email
            self.fields[User.first_name.field.name].initial = self.user.first_name
            self.fields[User.last_name.field.name].initial = self.user.last_name

        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    def clean_birthday(self):
        birth_date = self.cleaned_data.get('birthday')
        if not birth_date:
            return birth_date

        today = datetime.date.today()
        if birth_date >= today:
            raise ValidationError(
                _(
                    'Дата рождения не может быть в будущем. Введите корректную дату.',
                ),
            )

        max_age = today.replace(year=today.year - 120)
        if birth_date < max_age:
            raise ValidationError(
                _(
                    'Вы, оказывается, долгожитель ;) Мы не верим. Введите корректную дату.',
                ),
            )

        return birth_date

    class Meta:
        model = Profile
        fields = [
            Profile.birthday.field.name,
            Profile.image.field.name,
        ]
        widgets = {
            Profile.birthday.field.name: forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
        help_texts = {
            Profile.image.field.name: _(
                'загрузите изображение вашего профиля',
            ),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        try:
            if self.user:
                self.user.email = self.cleaned_data.get('email')
                self.user.first_name = self.cleaned_data.get('first_name')
                self.user.last_name = self.cleaned_data.get('last_name')
                self.user.save()
        except ValidationError:
            return None

        if commit:
            profile.save()

        return profile


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    error_messages = {
        'invalid_login': 'Пожалуйста, введите правильные имя пользователя'
        ' и пароль. Оба поля могут быть чувствительны к регистру.',
        'inactive': 'Этот аккаунт неактивен.',
    }
    username = forms.CharField(label=_('Логин или почта'))
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _('Пользователь с таким email уже существует.'),
                code='duplicate_code',
            )

        return email

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )

        return super().clean()
