__all__ = (
    'ChangeForm',
    'LoginForm',
    'ProfileForm',
    'SignupForm',
    'UserForm',
)

import datetime

import django
import django.contrib.auth
import django.contrib.auth.forms
import django.core.exceptions
from django.utils.translation import gettext_lazy as _

import users.models

User = django.contrib.auth.get_user_model()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            if isinstance(field.widget, django.forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignupForm(BootstrapFormMixin, django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        required=True,
        widget=django.forms.EmailInput(attrs={'class': 'form-control'}),
        label=_('Почта'),
    )
    accept_terms = django.forms.BooleanField(
        required=True,
        label=_('Я согласен с условиями использования'),
        widget=django.forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': _('Вы должны принять условия использования')},
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User
        exclude = (User.first_name.field.name,)
        fields = django.contrib.auth.forms.UserCreationForm.Meta.fields + (
            User.email.field.name,
            'accept_terms',
        )
        labels = {
            User.username.field.name: _('Логин'),
            User.email.field.name: _('Почта'),
            'accept_terms': _('Я согласен с условиями использования'),
        }
        help_text = {
            User.username.field.name: _('Введите логин'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise django.core.exceptions.ValidationError(
                _('Пользователь с таким email уже существует.'),
                code='duplicate_code',
            )

        return email

    def clean_accept_terms(self):
        accepted = self.cleaned_data.get('accept_terms')
        if not accepted:
            raise django.core.exceptions.ValidationError(
                _('Вы должны принять условия использования'),
                code='required',
            )

        return accepted

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()

        return user


class ChangeForm(BootstrapFormMixin, django.contrib.auth.forms.UserChangeForm):
    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = User
        fields = django.contrib.auth.forms.UserChangeForm.Meta.fields


class UserForm(BootstrapFormMixin, django.forms.ModelForm):
    class Meta:
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
        )


class ProfileForm(django.forms.ModelForm):
    first_name = django.forms.CharField(max_length=150, required=False, label=_('Имя'))
    last_name = django.forms.CharField(max_length=150, required=False, label=_('Фамилия'))
    email = django.forms.EmailField(label=_('Email'))

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
            raise django.core.exceptions.ValidationError(
                _(
                    'Дата рождения не может быть в будущем. Введите корректную дату.',
                ),
            )

        max_age = today.replace(year=today.year - 120)
        if birth_date < max_age:
            raise django.core.exceptions.ValidationError(
                _(
                    'Вы, оказывается, долгожитель ;) Мы не верим. Введите корректную дату.',
                ),
            )

        return birth_date

    class Meta:
        model = users.models.Profile
        fields = [
            users.models.Profile.birthday.field.name,
            users.models.Profile.location.field.name,
            users.models.Profile.image.field.name,
        ]
        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }
        help_texts = {
            users.models.Profile.image.field.name: _(
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
        except django.core.exceptions.ValidationError:
            return None

        if commit:
            profile.save()

        return profile


class LoginForm(BootstrapFormMixin, django.contrib.auth.forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Пожалуйста, введите правильные имя пользователя'
        ' и пароль. Оба поля могут быть чувствительны к регистру.',
        'inactive': 'Этот аккаунт неактивен.',
    }
    username = django.forms.CharField(label=_('Логин или почта'))
    password = django.forms.CharField(
        label=_('Пароль'),
        widget=django.forms.PasswordInput,
        required=True,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise django.core.exceptions.ValidationError(
                _('Пользователь с таким email уже существует.'),
                code='duplicate_code',
            )

        return email

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise django.core.exceptions.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )

        return super().clean()
