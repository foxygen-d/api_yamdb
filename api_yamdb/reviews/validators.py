from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Нельзя указать год больше текущего'
        )
    return value
