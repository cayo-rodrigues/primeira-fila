import uuid

from django.db import models


# Create your models here.
class Cinema(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="cinemas"
    )
    address = models.OneToOneField(
        "addresses.Address",
        on_delete=models.CASCADE,
        related_name="cinemas",
    )
