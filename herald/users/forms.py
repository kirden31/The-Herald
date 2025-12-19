__all__ = (
    'LoginForm',
    'ProfileForm',
    'SignupForm',
)

import datetime

import django
import django.contrib.auth
import django.contrib.auth.forms
import django.core.exceptions
import django.forms
from django.utils.translation import gettext_lazy

import news.forms_data
import users.models

User = django.contrib.auth.get_user_model()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if isinstance(field.widget, django.forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignupForm(BootstrapFormMixin, django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        error_messages={'required': gettext_lazy('Пользователь с такой почтой уже существует')},
        label=gettext_lazy('Mail'),
    )
    accept_terms = django.forms.BooleanField(
        required=True,
        label=gettext_lazy('Я согласен с условиями использования'),
        error_messages={'required': gettext_lazy('Вы должны принять условия использования')},
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User

        fields = (
            users.models.User.username.field.name,
            users.models.User.email.field.name,
            'accept_terms',
        )

        labels = {
            users.models.User.username.field.name: gettext_lazy('Login'),
            users.models.User.email.field.name: gettext_lazy('Email'),
            'accept_terms': gettext_lazy('I_agree_to_the_terms_of_use'),
        }

        help_text = {
            users.models.User.username.field.name: gettext_lazy('Enter_login'),
            users.models.User.email.field.name: gettext_lazy('Enter_email'),
        }

    def clean_accept_terms(self):
        accepted = self.cleaned_data.get('accept_terms')
        if not accepted:
            raise django.core.exceptions.ValidationError(
                gettext_lazy('Для регистрации вы должны принять условия использования'),
                code='required',
            )

        return accepted


class ProfileForm(BootstrapFormMixin, django.forms.ModelForm):
    first_name = django.forms.CharField(
        max_length=150,
        required=False,
        label=gettext_lazy('Имя'),
    )
    last_name = django.forms.CharField(
        max_length=150,
        required=False,
        label=gettext_lazy('Фамилия'),
    )
    email = django.forms.EmailField(
        label=gettext_lazy('Email'),
    )
    favorite_categories = django.forms.MultipleChoiceField(
        choices=news.forms_data.CATEGORIES_CHOICES,
        widget=django.forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label=gettext_lazy('Favorite categories'),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['favorite_categories'].initial = self.user.profile.favorite_categories

    class Meta:
        model = users.models.Profile

        fields = (
            users.models.Profile.birthday.field.name,
            users.models.Profile.location.field.name,
            users.models.Profile.image.field.name,
            users.models.Profile.favorite_categories.field.name,
        )

        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={'type': 'date', 'max': datetime.date.today()},
                format='%Y-%m-%d',
            ),
        }

        help_texts = {
            users.models.Profile.image.field.name: gettext_lazy(
                'Upload your profile picture',
            ),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']
        self.user.profile.favorite_categories = self.cleaned_data['favorite_categories']

        if commit:
            self.user.save()
            profile.save()

        return profile


class LoginForm(BootstrapFormMixin, django.contrib.auth.forms.AuthenticationForm):
    error_messages = {
        'invalid_login': 'Пожалуйста, введите правильные имя пользователя'
        ' и пароль. Оба поля могут быть чувствительны к регистру.',
        'inactive': 'Этот аккаунт неактивен.',
    }
    username = django.forms.CharField(label=gettext_lazy('Login or email'))
    password = django.forms.CharField(
        label=gettext_lazy('Password'),
        widget=django.forms.PasswordInput,
        required=True,
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            raise django.core.exceptions.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
            )

        return super().clean()
