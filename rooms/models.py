import uuid

from django.db import models

# Create your models here.


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    cinema = models.ForeignKey(
        "cinemas.Cinema", on_delete=models.CASCADE, related_name="rooms"
    )


class SeatRows(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    row = models.CharField(max_length=20)
    seat_count = models.PositiveIntegerField()
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="seat_rows", null=True
    )


class RoomCorridor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    column = models.IntegerField()
    from_row = models.IntegerField()
    to_row = models.IntegerField()
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="room_corridors", null=True
    )


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=5)
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="seats"
    )
