from django.db import models
import uuid
from utils.validators import PriceValidators

# Create your models here.

class UserFinancialControl(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="financial_control"
    )
    
class CinemaFinancialControl(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    expenses = models.DecimalField(
        default=0.00,
        validators=[PriceValidators.validate_positive],
        max_digits=20,
        decimal_places=2
    )
    income = models.DecimalField(
        default=0.00,
        validators=[PriceValidators.validate_positive],
        max_digits=20,
        decimal_places=2
    )
    cinema = models.OneToOneField(
        "cinemas.Cinema", on_delete=models.CASCADE, related_name="financial_control"
    )    