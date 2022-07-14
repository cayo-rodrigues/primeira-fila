from django.db import models

# Create your models here.
class Cinema(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="cinemas"
    )
    address = models.OneToOneField(
        "addresses.Address",
        on_delete=models.CASCADE,
        related_name="cinemas",
    )
    # rooms = models.ForeignKey(
    #     "rooms.Room", on_delete=models.CASCADE, related_name="rooms"
    # )
    # movies_cinemas = models.ForeignKey(
    #     "movies.Movie", on_delete=models.CASCADE, related_name="movies"
    # )
