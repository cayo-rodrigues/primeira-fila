from django.core.exceptions import ValidationError
from django.utils import timezone


class PriceValidators:
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


class UploadValidators:
    def validate_file_size(value):
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise ValidationError("File too large. Size should not exceed 2 MB.")
