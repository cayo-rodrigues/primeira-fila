from cinemas.models import Cinema
from rest_framework import serializers, status

from rooms.models import Room, RoomCorridor, SeatRows
from tickets.models import Seat


class SeatRowsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = SeatRows
        exclude = ["room"]


class RoomCorridorsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

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


class UpdateSeatRowsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = SeatRows
        exclude = ["room"]


class UpdateRoomCorridorsSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()

    class Meta:
        model = RoomCorridor
        exclude = ["room"]


class UpdateRoomSerializer(serializers.ModelSerializer):
    seat_rows = UpdateSeatRowsSerializer(many=True)
    room_corridors = UpdateRoomCorridorsSerializer(many=True)

    class Meta:
        model = Room
        fields = ["id", "name", "seat_rows", "room_corridors"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)

        corridors = validated_data.pop("room_corridors", None)
        rows = validated_data.pop("seat_rows", None)

        if corridors:
            try:
                corridor_id_map = [corridor["id"] for corridor in corridors]
                all_corridors = RoomCorridor.objects.filter(room=instance)
                corridors_in_instance = {
                    corridor.id: corridor for corridor in all_corridors
                }

                for corridor_id, corridor in corridors_in_instance.items():
                    if corridor_id not in corridor_id_map:
                        corridor.delete()
            except:
                pass

            for value in corridors:
                try:
                    old_corridor = RoomCorridor.objects.get(pk=value["id"])
                except:
                    old_corridor = None

                if old_corridor is not None:
                    old_corridor.column = value["column"]
                    old_corridor.from_row = value["from_row"]
                    old_corridor.to_row = value["to_row"]
                    old_corridor.save()
                else:
                    room_corridor = RoomCorridor.objects.create(**value)
                    instance.room_corridors.add(room_corridor)

        if rows:
            try:
                seat_row_id_map = [row["id"] for row in rows]
                all_seats_rows = SeatRows.objects.filter(room=instance)
                seats_row_in_instance = {row.id: row for row in all_seats_rows}

                for row_id, row in seats_row_in_instance.items():
                    if row_id not in seat_row_id_map:
                        row.delete()
            except:
                pass

            for value in rows:
                try:
                    old_row = SeatRows.objects.get(pk=value["id"])
                except:
                    old_row = None

                if old_row is not None:
                    all_seats = Seat.objects.filter(room=instance)
                    print(all_seats)
                    old_row.row = value["row"]
                    old_row.seat_count = value["seat_count"]
                    old_row.save()
                else:
                    seat_rows = SeatRows.objects.create(**value)
                    instance.seat_rows.add(seat_rows)

                    for i in range(seat_rows.seat_count):
                        name = f"{seat_rows.row}{i+1}"
                        new_seat = {"name": name, "room": instance}
                        created_seat = Seat.objects.create(**new_seat)
                        created_seat.save()

        instance.save()
        return instance
