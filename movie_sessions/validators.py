from django.core.exceptions import ValidationError


class PriceValidators:
    def validate_positive(value):
        if value < 0:
            raise ValidationError(
                ("%(value)s is not an posivite number"),
                params={"value": value},
            )
