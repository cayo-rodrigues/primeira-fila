from uuid import uuid4

from django.db import models


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="tickets"
    )

    movie_session = models.ForeignKey(
        "movie_sessions.MovieSession", on_delete=models.CASCADE, related_name="tickets"
    )


class SessionSeat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    is_avaliable = models.BooleanField(default=True)

    seat = models.ForeignKey(
        "tickets.Seat", on_delete=models.CASCADE, related_name="session_seats"
    )

    ticket = models.ForeignKey(
        "tickets.Ticket", on_delete=models.CASCADE, related_name="session_seats"
    )

    movie_session = models.ForeignKey(
        "movie_sessions.MovieSession",
        on_delete=models.CASCADE,
        related_name="session_seats",
    )


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=5)

    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="seats"
    )
