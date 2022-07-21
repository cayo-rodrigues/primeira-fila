from movie_sessions.models import SessionSeat
from rest_framework import serializers

from rooms.models import Room, RoomCorridor, Seat, SeatRows


class SeatRowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatRows
        exclude = ["room"]


class RoomCorridorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCorridor
        exclude = ["room"]


class RoomSerializer(serializers.ModelSerializer):
    seat_rows = SeatRowsSerializer(many=True)
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
            seat = SeatRows(**value, room=room)
            seat_rows.append(seat)

            for i in range(seat.seat_count):
                name = f"{seat.row}{i+1}"
                new_seat = {"name": name, "room": room}
                seat_instances.append(Seat(**new_seat))

        SeatRows.objects.bulk_create(seat_rows)
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

        if corridors:
            new_corridors = []
            for value in corridors:
                new_corridors.append(RoomCorridor(**value))

            instance.room_corridors.set(RoomCorridor.objects.bulk_create(new_corridors))

        if rows:
            new_rows = []
            new_seats = []
            for value in rows:
                seat_rows = SeatRows(**value)
                new_rows.append(seat_rows)
                all_seats_in_instance = Seat.objects.filter(room=instance)

                all_sessions_seats = SessionSeat.objects.all()

                for seat in all_sessions_seats:
                    for seat_instance in all_seats_in_instance:
                        if seat.seat == seat_instance and not seat.is_available:
                            raise serializers.ValidationError(
                                {
                                    "message": f"{seat.seat.name} is already with a movie session."
                                }
                            )

                for value in all_seats_in_instance:
                    value.delete()

                for i in range(seat_rows.seat_count):
                    name = f"{seat_rows.row}{i+1}"
                    new_seat = {"name": name, "room": instance}
                    new_seats.append(Seat(**new_seat))

            instance.seat_rows.set(SeatRows.objects.bulk_create(new_rows))
            Seat.objects.bulk_create(new_seats)

        instance.save()
        return instance
