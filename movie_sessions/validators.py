from django.core.exceptions import ValidationError
from django.utils import timezone

class ProductValidators:
    def validate_positive(value):
        if value < 0:
            raise ValidationError(
                ("%(value)s is not an posivite number"),
                params={"value": value},
            )


class DateValidators:
    def session_day_cannot_be_before_today(value):
        if value < timezone.now():
            raise ValidationError(
                ("%(value)s is a invalid date"),
                params={"value": value},
            )
