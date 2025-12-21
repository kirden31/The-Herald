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
from django.utils.translation import gettext_lazy as _

import news.forms_data
import users.models

User = django.contrib.auth.get_user_model()


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for __, field in self.fields.items():
            if isinstance(field.widget, django.forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class SignupForm(BootstrapFormMixin, django.contrib.auth.forms.UserCreationForm):
    email = django.forms.EmailField(
        label=_('Mail'),
    )

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User

        fields = (
            users.models.User.username.field.name,
            users.models.User.email.field.name,
        )

        labels = {
            users.models.User.username.field.name: _('Login'),
            users.models.User.email.field.name: _('Email'),
        }

        help_text = {
            users.models.User.username.field.name: _('Enter_login'),
            users.models.User.email.field.name: _('Enter_email'),
        }


class ProfileForm(BootstrapFormMixin, django.forms.ModelForm):
    first_name = django.forms.CharField(
        max_length=150,
        required=False,
        label=_('Name'),
    )
    last_name = django.forms.CharField(
        max_length=150,
        required=False,
        label=_('Surname'),
    )
    email = django.forms.EmailField(
        label=_('Email'),
    )
    favorite_categories = django.forms.MultipleChoiceField(
        choices=news.forms_data.CATEGORIES_CHOICES,
        widget=django.forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label=_('Favorite_categories'),
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
            users.models.Profile.image.field.name: _('Upload_your_profile_picture'),
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
        'invalid_login': _(
            'invalid_login_text',
        ),
        'inactive': _('This_account_is_inactive'),
    }
    username = django.forms.CharField(label=_('Login or email'))
    password = django.forms.CharField(
        label=_('Password'),
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
