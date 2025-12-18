__all__ = ('ValidateBirthdayDate',)

import datetime

import django.core.exceptions
import django.utils.deconstruct
import django.utils.timezone
from django.utils.translation import gettext as _


@django.utils.deconstruct.deconstructible
class ValidateBirthdayDate:
    def __init__(self, max_age_years=150):
        self.max_age_years = max_age_years

    def __call__(self, date_value):
        current_date = django.utils.timezone.now().date()
        earliest_date = current_date - datetime.timedelta(
            days=self.max_age_years * 365,
        )

        if not earliest_date <= date_value <= current_date:
            raise django.core.exceptions.ValidationError(
                _('birthday_date_error'),
            )

        return date_value
