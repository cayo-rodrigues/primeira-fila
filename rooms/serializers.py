from rest_framework import serializers
from cinemas.models import Cinema
from rest_framework import status

from rooms.models import Room, RoomCorridor, SeatRows


class SeatRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRows
        fields = ["row", "seat_count"]


class RoomCorridorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCorridor
        exclude = ["id", "room"]


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    seat_rows = SeatRowsSerializer(many=True)
    room_corridors = RoomCorridorsSerializer(many=True)

    class Meta:
        model = Room
        fields = ["id", "name", "seat_rows", "room_corridors"]

    def create(self, validated_data):

        cine_id = (
            self.context.get("request").parser_context.get("kwargs").get("cine_id")
        )

        try:
            cinema = Cinema.objects.filter(pk=cine_id)[0]
        except:
            raise serializers.ValidationError(
                detail={"detail": "Cinema not found"}, code=404
            )

        seats = validated_data.pop("seat_rows")
        corridors_list = validated_data.pop("room_corridors")

        room = Room.objects.create(**validated_data)

        room.cinema = cinema

        for value in seats:
            seat = SeatRows.objects.create(**value)
            seat.room = room
            seat.save()

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

        instance.save()
        return instance
