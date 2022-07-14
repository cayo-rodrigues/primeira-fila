from cinemas.models import Cinema
from rest_framework import serializers, status

from rooms.models import Room, RoomCorridor, SeatRows
from tickets.models import Seat


class SeatRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRows
        fields = ["row", "seat_count"]


class RoomCorridorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCorridor
        exclude = ["id", "room"]


class RoomSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(read_only=True)
    seat_rows = SeatRowsSerializer(many=True)
    room_corridors = RoomCorridorsSerializer(many=True)

    class Meta:
        model = Room
        fields = ["id", "name", "seat_rows", "room_corridors"]

    def create(self, validated_data):
        seats = validated_data.pop("seat_rows")
        corridors_list = validated_data.pop("room_corridors")

        room = Room.objects.create(**validated_data)

        for value in seats:
            seat = SeatRows.objects.create(**value)
            seat.room = room
            seat.save()
            for i in range(seat.seat_count):
                name = f"{seat.row}{i+1}"
                new_seat = {"name": name, "room": room}
                created_seat = Seat.objects.create(**new_seat)
                created_seat.save()

        for value in corridors_list:
            corridor = RoomCorridor.objects.create(**value)
            corridor.room = room
            corridor.save()

        room.save()

        return room

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        corridors = validated_data.pop("room_corridors", None)
        rows = validated_data.pop("seat_rows", None)

        if corridors:
            instance.room_corridors.set([])
            for value in corridors:
                room_corridor = RoomCorridor.objects.create(**value)
                instance.room_corridors.add(room_corridor)

        if rows:
            instance.seat_rows.set([])
            for value in rows:
                seat_rows = SeatRows.objects.create(**value)
                instance.seat_rows.add(seat_rows)

                for i in range(seat_rows.seat_count):
                    name = f"{seat_rows.row}{i+1}"
                    new_seat = {"name": name, "room": instance}
                    created_seat = Seat.objects.create(**new_seat)
                    created_seat.save()

        instance.save()
        return instance
