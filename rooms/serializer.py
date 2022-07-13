from unicodedata import name
from attr import fields
from rest_framework import serializers

from rooms.models import Room, RoomCorridor, SeatRows


class SeatRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRows
        fields = "__all__"


class RoomCorridorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCorridor
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    seat_rows = SeatRowsSerializer(many=True)
    corridors = RoomCorridorsSerializer(many=True)

    class Meta:
        model = Room
        fields = ["id", "name", "seat_rows", "corridors"]

    def create(self, validated_data):

        seats = validated_data.pop("seat_rows")
        corridors_list = validated_data.pop("corridors")

        room = Room.objects.create(**validated_data)

        for value in seats:
            seat = SeatRows.objects.create(**value)
            seat.room = room
            seat.save()

        for value in corridors_list:
            corridor = RoomCorridor.objects.create(**value)
            corridor.room = room
            corridor.save()

        return room
