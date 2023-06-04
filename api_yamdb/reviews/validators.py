from django.core.exceptions import ValidationError

import datetime as dt


MIN_YEAR = 0


def validate_year(value):
    year = dt.date.today().year
    if value > year or value < MIN_YEAR:
        raise ValidationError(
            'Необходимо проверить год публикации произведения!'
        )
