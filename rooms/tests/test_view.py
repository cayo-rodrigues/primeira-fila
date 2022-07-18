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
from rest_framework.test import APITestCase

from users.models import User


class RoomViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.room_data = {
            "name": "Teste meu nobre",
            "seat_rows": [
                {"row": "A", "seat_count": 2},
                {"row": "B", "seat_count": 2},
                {"row": "C", "seat_count": 2},
            ],
            "room_corridors": [
                {"column": 1, "from_row": 2, "to_row": 7},
                {"column": 8, "from_row": 2, "to_row": 7},
            ],
        }

        cls.room_update = {
            "name": "Outro teste meu nobre",
            "seat_rows": [
                {"row": "A", "seat_count": 5},
                {"row": "B", "seat_count": 5},
            ],
            "room_corridors": [
                {"column": 5, "from_row": 1, "to_row": 8},
                {"column": 77, "from_row": 99, "to_row": 99},
            ],
        }

        cls.manager_user = User.objects.create(
            email="teste2@teste.com",
            first_name="Teste",
            last_name="Teste",
            age=18,
            password="1234",
            is_staff=True,
        )

        cls.normal_user = User.objects.create(
            email="teste@teste.com",
            first_name="Teste",
            last_name="Teste",
            age=18,
            password="1234",
        )

        cls.normal_user.is_active = True
        cls.normal_user.save()

        cls.manager_user.is_active = True
        cls.manager_user.save()

        cls.name_data = DEFAULT_CINEMA_DATA
        cls.address_data = DEFAULT_ADDRESS_DATA
        cls.city_data = DEFAULT_CITY_DATA
        cls.district_data = DEFAULT_DISTRICT_DATA
        cls.state_data = DEFAULT_STATE_DATA
        cls.country_data = DEFAULT_COUNTRY_DATA

        cls.city = City.objects.create(**cls.city_data)
        cls.district = District.objects.create(**cls.district_data)
        cls.state = State.objects.create(**cls.state_data)
        cls.country = Country.objects.create(**cls.country_data)
        cls.address = Address.objects.create(
            **cls.address_data,
            city=cls.city,
            district=cls.district,
            state=cls.state,
            country=cls.country,
        )

        cls.cinema: Cinema = Cinema.objects.create(
            **cls.name_data, address=cls.address, owner=cls.manager_user
        )

    def setUp(self):
        response = self.client.post(
            "/sessions/token/",
            {"email": "teste2@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

    def test_can_list_all_rooms(self):
        response = self.client.get(f"/cinemas/{self.cinema.id}/")

        self.assertEqual(response.status_code, 200)

    def test_list_one_room_from_cinema(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        response = self.client.get(
            f"/cinemas/{self.cinema.id}/rooms/{response.data['id']}/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.room_data["name"])
        self.assertEqual(
            response.data["seat_rows"][0]["row"], self.room_data["seat_rows"][0]["row"]
        )
        self.assertEqual(
            response.data["room_corridors"][0]["column"],
            self.room_data["room_corridors"][0]["column"],
        )

    def test_list_return_values(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        response = self.client.get(f"/cinemas/{self.cinema.id}/rooms/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_manager_user_can_create_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        self.assertEqual(response.status_code, 201)

    def test_user_not_owner_of_cinema_cant_create_room(self):
        response = self.client.post(
            "/sessions/token/",
            {"email": "teste@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_delete_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )
        response = self.client.delete(
            f"/cinemas/{self.cinema.id}/rooms/{response.data['id']}/"
        )

        self.assertEqual(response.status_code, 204)

    def test_not_manager_user_cant_delete_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        room = response.data["id"]

        response = self.client.post(
            "/sessions/token/",
            {"email": "teste@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

        response = self.client.delete(f"/cinemas/{self.cinema.id}/rooms/{room}/")

        self.assertEqual(response.status_code, 403)

    def test_manager_can_update_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )
        response = self.client.patch(
            f"/cinemas/{self.cinema.id}/rooms/{response.data['id']}/",
            self.room_update,
            "json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], self.room_update["name"])
        self.assertEqual(
            response.data["seat_rows"][0]["row"],
            self.room_update["seat_rows"][0]["row"],
        )
        self.assertEqual(
            response.data["room_corridors"][0]["column"],
            self.room_update["room_corridors"][0]["column"],
        )

    def test_normal_user_cant_update_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.id}/rooms/", self.room_data, "json"
        )

        room = response.data["id"]

        response = self.client.post(
            "/sessions/token/",
            {"email": "teste@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

        response = self.client.patch(
            f"/cinemas/{self.cinema.id}/rooms/{room}/",
            self.room_update,
            "json",
        )

        self.assertEqual(response.status_code, 403)
