from django.test import TestCase

from rooms.models import Room, RoomCorridors, SeatRows


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = "Sala 1"
        cls.column = 1
        cls.from_row = 2
        cls.to_row = 7
        cls.rows = 2

        cls.room = Room.objects.create(name=cls.name)

        cls.seat_rows = SeatRows.objects.create(row="A", seat_count=5, room=cls.room)

        cls.corridors = RoomCorridors.objects.create(
            column=cls.column, from_row=cls.from_row, to_row=cls.to_row, room=cls.room
        )

        cls.room_id = cls.room.id
        cls.seat_rows_id = cls.seat_rows.id
        cls.corridors_id = cls.corridors.id

    def test_room_exists(self):
        room = Room.objects.get(id=self.room_id)

        self.assertIsNotNone(room)

    def test_not_null_room_fields(self):
        room = Room.objects.get(id=self.room_id)

        self.assertIsNotNone(room.name)

    def test_seat_rows_exist(self):
        seat_rows = SeatRows.objects.get(id=self.seat_rows_id)

        self.assertIsNotNone(seat_rows)

    def test_seat_rows_correct_fields(self):
        seat_rows = SeatRows.objects.get(id=self.seat_rows_id)
        room = Room.objects.get(id=self.room_id)

        self.assertEquals(seat_rows.row, "A")
        self.assertEquals(seat_rows.seat_count, 5)
        self.assertEquals(seat_rows.room, room)

    def test_corridors_exist(self):
        corridors = RoomCorridors.objects.get(id=self.corridors_id)

        self.assertIsNotNone(corridors)

    def test_corridors_fields(self):
        corridors = RoomCorridors.objects.get(id=self.corridors_id)
        room = Room.objects.get(id=self.room_id)

        self.assertEquals(corridors.column, self.column)
        self.assertEquals(corridors.from_row, self.from_row)
        self.assertEquals(corridors.to_row, self.to_row)
        self.assertEquals(corridors.room, room)
