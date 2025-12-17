from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_future_date(value):
    if value and value < timezone.localdate():
        raise ValidationError("End date cannot be in the past.")
