from rest_framework import serializers
from movie_sessions.models import MovieSession, SessionSeat

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
            # try:
            #     corridor_id_map = [corridor["column"] for corridor in corridors]
            #     all_corridors = RoomCorridor.objects.filter(room=instance)
            #     corridors_in_instance = {
            #         corridor.id: corridor for corridor in all_corridors
            #     }

            #     for corridor_id, corridor in corridors_in_instance.items():
            #         if corridor_id not in corridor_id_map:
            #             corridor.delete()
            # except:
            #     pass

            new_corridors = []
            for value in corridors:
                # try:
                #     old_corridor = RoomCorridor.objects.get(pk=value["column"])
                # except:
                #     old_corridor = None

                # if old_corridor is not None:
                #     old_corridor.column = value["column"]
                #     old_corridor.from_row = value["from_row"]
                #     old_corridor.to_row = value["to_row"]
                #     old_corridor.save()
                # else:
                new_corridors.append(RoomCorridor(**value))

            instance.room_corridors.set(RoomCorridor.objects.bulk_create(new_corridors))

        if rows:
            # try:
            #     seat_row_id_map = [row["row"] for row in rows]
            #     all_seats_rows = SeatRows.objects.filter(room=instance)
            #     seats_row_in_instance = {row.id: row for row in all_seats_rows}

            #     for row_id, row in seats_row_in_instance.items():
            #         if row_id not in seat_row_id_map:
            #             row.delete()

            # except:
            #     pass

            new_rows = []
            new_seats = []
            for value in rows:
                # try:
                #     old_row = SeatRows.objects.get(row=value["row"], room=instance)
                #     print(old_row)
                # except:
                #     old_row = None

                # if old_row is not None:
                #     all_seats = Seat.objects.filter(room=instance)
                #     print("chegou aqui senhor?")
                #     old_row[0].row = value["row"]
                #     old_row[0].seat_count = value["seat_count"]
                #     old_row[0].save()
                # else:
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
