from django.core.exceptions import ValidationError

import datetime as dt


def validate_year(value):
    year = dt.date.today().year
    if value > year or value < 0:
        raise ValidationError(
            'Необходимо проверить год публикации произведения!'
        )
