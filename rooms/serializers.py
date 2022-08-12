from movie_sessions.models import SessionSeat
from rest_framework import serializers
from utils.helpers import bulk_get_or_create, set_and_destroy

from rooms.models import Room, RoomCorridor, Seat, SeatRow


class SeatRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRow
        exclude = ["room"]


class RoomCorridorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCorridor
        exclude = ["room"]


class RoomSerializer(serializers.ModelSerializer):
    seat_rows = SeatRowSerializer(many=True)
    room_corridors = RoomCorridorsSerializer(many=True)

    class Meta:

        model = Room
        fields = ["id", "name", "seat_rows", "room_corridors"]

    def create(self, validated_data):
        seats = validated_data.pop("seat_rows")
        corridors_list = validated_data.pop("room_corridors")

        room = Room.objects.create(**validated_data)

        seat_rows = []
        seat_instances = []
        for value in seats:
            seat = SeatRow(**value, room=room)
            seat_rows.append(seat)

            for i in range(seat.seat_count):
                name = f"{seat.row}{i+1}"
                new_seat = {"name": name, "room": room}
                seat_instances.append(Seat(**new_seat))

        SeatRow.objects.bulk_create(seat_rows)
        Seat.objects.bulk_create(seat_instances)

        RoomCorridor.objects.bulk_create(
            [RoomCorridor(**value, room=room) for value in corridors_list]
        )

        room.save()

        return room

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        corridors = validated_data.pop("room_corridors", None)
        rows = validated_data.pop("seat_rows", None)

        if instance.movie_sessions.filter(on_sale=True).exists():
            raise serializers.ValidationError(
                {"detail": "Can't update room when it has movie sessions on sale"}
            )

        if corridors:
            set_and_destroy(
                klass=instance,
                attr="room_corridors",
                value=bulk_get_or_create(RoomCorridor, corridors, room=instance),
                related_klass=RoomCorridor,
                room=None,
            )

        if rows:
            seats_to_create = []
            existing_seats = []

            for value in rows:
                for i in range(value["seat_count"]):
                    name = f"{value['row']}{i+1}"
                    new_seat = {"name": name, "room": instance}
                    seats_found = Seat.objects.filter(**new_seat)
                    if seats_found:
                        existing_seats.extend(seats_found)
                    else:
                        seats_to_create.append(Seat(**new_seat))

            set_and_destroy(
                klass=instance,
                attr="seat_rows",
                value=bulk_get_or_create(SeatRow, rows, room=instance),
                related_klass=SeatRow,
                room=None,
            )
            set_and_destroy(
                klass=instance,
                attr="seats",
                value=Seat.objects.bulk_create(seats_to_create) + existing_seats,
                related_klass=Seat,
                room=None,
            )

        instance.save()
        return instance
