import uuid

from django.db import models
from .validators import PriceValidators, DateValidators


class MovieSession(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    price = models.DecimalField(
        validators=[PriceValidators.validate_positive, DateValidators.session_day_cannot_be_before_today],
        max_digits=10,
        decimal_places=2,
    )
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


class SessionSeat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_available = models.BooleanField(default=True)

    seat = models.ForeignKey(
        "rooms.Seat", on_delete=models.CASCADE, related_name="session_seats"
    )

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        related_name="session_seats",
        null=True,
    )

    movie_session = models.ForeignKey(
        "movie_sessions.MovieSession",
        on_delete=models.CASCADE,
        related_name="session_seats",
    )
