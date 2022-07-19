from django.test import TestCase
from addresses.models import Address, City, Country, District, State
from cinemas.models import Cinema
from cinemas.tests.util import (
    DEFAULT_ADDRESS_DATA,
    DEFAULT_CINEMA_DATA,
    DEFAULT_CITY_DATA,
    DEFAULT_COUNTRY_DATA,
    DEFAULT_DISTRICT_DATA,
    DEFAULT_STATE_DATA,
)

from rooms.models import Room, RoomCorridor, SeatRows
from users.models import User


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.name = "Sala 1"
        cls.column = 1
        cls.from_row = 2
        cls.to_row = 7
        cls.rows = 2

        cls.name_data = DEFAULT_CINEMA_DATA
        cls.address_data = DEFAULT_ADDRESS_DATA
        cls.city_data = DEFAULT_CITY_DATA
        cls.district_data = DEFAULT_DISTRICT_DATA
        cls.state_data = DEFAULT_STATE_DATA
        cls.country_data = DEFAULT_COUNTRY_DATA

        cls.user_manager = User.objects.create(
            email="gerente@mail.com",
            password="1234",
            first_name="Gerente",
            last_name="da Silva",
            age=40,
            is_staff=True,
        )

        cls.city = City.objects.create(**cls.city_data)
        cls.district = District.objects.create(**cls.district_data)
        cls.state = State.objects.create(**cls.state_data)
        cls.country = Country.objects.create(**cls.country_data)
        cls.address = Address.objects.create(
            **cls.address_data,
            city=cls.city,
            district=cls.district,
            state=cls.state,
            country=cls.country
        )

        cls.cinema = Cinema.objects.create(
            **cls.name_data, address=cls.address, owner=cls.user_manager
        )

        cls.room = Room.objects.create(name=cls.name, cinema=cls.cinema)

        cls.seat_rows = SeatRows.objects.create(row="A", seat_count=5, room=cls.room)

        cls.corridors = RoomCorridor.objects.create(
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
        corridors = RoomCorridor.objects.get(id=self.corridors_id)

        self.assertIsNotNone(corridors)

    def test_corridors_fields(self):
        corridors = RoomCorridor.objects.get(id=self.corridors_id)
        room = Room.objects.get(id=self.room_id)

        self.assertEquals(corridors.column, self.column)
        self.assertEquals(corridors.from_row, self.from_row)
        self.assertEquals(corridors.to_row, self.to_row)
        self.assertEquals(corridors.room, room)
