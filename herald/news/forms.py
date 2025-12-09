__all__ = ('SearchForm',)

import django.forms
from django.utils.translation import gettext_lazy as _


class SearchForm(django.forms.Form):
    query = django.forms.CharField(
        label=_('Search'),
        max_length=500,
        required=True,
        widget=django.forms.TextInput(
            attrs={
                'placeholder': _('search_area_placeholder'),
                'aria-label': _('search_area'),
                'class': 'form-control',
            },
        ),
    )
