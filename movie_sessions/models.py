from django.db import models
import uuid


class MovieSession(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    price = models.DecimalField(max_digits=4, decimal_places=4)
    session_datetime = models.DateTimeField()
    subtitled = models.BooleanField()
    is_3d = models.BooleanField()
    on_sale = models.BooleanField()

    cinema = models.ForeignKey(
        "cinemas.Cinema", on_delete=models.CASCADE, related_name="movie_sessions"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        "movies.Movie", on_delete=models.CASCADE, related_name="movie_sessions"
    )
