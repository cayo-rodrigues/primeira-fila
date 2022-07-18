from django.test import TestCase
from addresses.models import Address, City, District, State, Country
from cinemas.models import Cinema
from users.models import User
from cinemas.tests.util import (
    DEFAULT_ADDRESS_DATA,
    DEFAULT_CINEMA_DATA,
    DEFAULT_CITY_DATA,
    DEFAULT_DISTRICT_DATA,
    DEFAULT_STATE_DATA,
    DEFAULT_COUNTRY_DATA,
)


class CinemaModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
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

        cls.cinema: Cinema = Cinema.objects.create(
            **cls.name_data, address=cls.address, owner=cls.user_manager
        )

    def test_can_create_cinema(self):
        self.assertTrue(bool(self.cinema))

    def test_if_cinema_has_all_fields(self):
        self.assertEqual(self.cinema.name, self.name_data["name"])

        self.assertIs(self.cinema.address, self.address)
        self.assertIs(self.cinema.address.city, self.city)
        self.assertIs(self.cinema.address.district, self.district)
        self.assertIs(self.cinema.address.state, self.state)
        self.assertIs(self.cinema.address.country, self.country)
