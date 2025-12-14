__all__ = ('EverythingFiltersForm', 'SourcesFilterForm', 'TopHeadlinesFilterForm', 'SearchForm')

import datetime

import django.forms
import django.utils.timezone
from django.utils.translation import gettext_lazy as _

import news.forms_data


class SearchForm(django.forms.Form):
    query = django.forms.CharField(
        label=_('Search'),
        max_length=500,
        required=False,
        empty_value='',
        widget=django.forms.TextInput(
            attrs={
                'placeholder': _('search_area_placeholder'),
                'aria-label': _('search_area'),
                'class': 'form-control',
            },
        ),
    )


class EverythingFiltersForm(django.forms.Form):
    search_in = django.forms.MultipleChoiceField(
        label=_('Search_in'),
        initial=(news.forms_data.TITLE, news.forms_data.DESCRIPTION, news.forms_data.CONTENT),
        choices=news.forms_data.SEARCH_IN_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    sources = django.forms.MultipleChoiceField(
        label=_('Select_sources_max_20_default_all'),
        choices=news.forms_data.SOURCES_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
                'max': 20,
            },
        ),
        required=False,
    )

    max_date = django.utils.timezone.now().date() - datetime.timedelta(days=1)
    min_date = django.utils.timezone.now().date() - datetime.timedelta(days=30)

    _from = django.forms.DateField(
        label=_('News_from'),
        widget=django.forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': max_date.isoformat(),
                'min': min_date.isoformat(),
            },
        ),
        required=False,
    )

    to = django.forms.DateField(
        label=_('News_to'),
        widget=django.forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': max_date.isoformat(),
                'min': min_date.isoformat(),
            },
        ),
        required=False,
    )

    language = django.forms.MultipleChoiceField(
        label=_('Select_language_default_all'),
        choices=news.forms_data.LANGUAGE_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )


class TopHeadlinesFilterForm(django.forms.Form):
    country = django.forms.MultipleChoiceField(
        label=_('Select_countries_default_all'),
        choices=news.forms_data.COUNTRIES_CHOICES_NEWS,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    category = django.forms.MultipleChoiceField(
        label=_('Select_countries_default_all'),
        choices=news.forms_data.CATEGORIES_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    sources = django.forms.MultipleChoiceField(
        label=_('Select_sources_default_all'),
        choices=news.forms_data.SOURCES_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
                'max': 20,
            },
        ),
        required=False,
    )


class SourcesFilterForm(django.forms.Form):
    language = django.forms.MultipleChoiceField(
        label=_('Select_language_default_all'),
        choices=news.forms_data.LANGUAGE_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    category = django.forms.MultipleChoiceField(
        label=_('Select_categories_default_all'),
        choices=news.forms_data.CATEGORIES_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    country = django.forms.MultipleChoiceField(
        label=_('Select_countries_default_all'),
        choices=news.forms_data.COUNTRIES_CHOICES_SOURCES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
                'max': 20,
            },
        ),
        required=False,
    )


class GuardianFiltersForm(django.forms.Form):
    section = django.forms.MultipleChoiceField(
        label=_('Sections'),
        choices=news.forms_data.SECTIONS_CHOICES,
        widget=django.forms.SelectMultiple(
            attrs={
                'class': 'js-example-basic-multiple',
                'style': 'width: 100%;',
            },
        ),
        required=False,
    )

    star_rating = django.forms.ChoiceField(
        label=_('Rating'),
        choices=news.forms_data.RATING_CHOICES,
        required=False,
    )

    max_date = django.utils.timezone.now().date()

    _from = django.forms.DateField(
        label=_('News_from'),
        widget=django.forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': max_date.isoformat(),
            },
        ),
        required=False,
    )

    to = django.forms.DateField(
        label=_('News_to'),
        widget=django.forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'max': max_date.isoformat(),
            },
        ),
        required=False,
    )
