__all__ = ('ValidateBirthdayDate','ValidateMaxFileSize')

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

@django.utils.deconstruct.deconstructible
class ValidateMaxFileSize:
    def __init__(self, max_size_mb=7):
        self.max_size_mb = max_size_mb
        self.max_size_byte = max_size_mb * 1024 * 1024

    def __call__(self, value):
        if value.size > self.max_size_byte:
            raise django.core.exceptions.ValidationError(
                _('Max_file_size_limit') + f'{self.max_size_mb}',
            )

        return value
