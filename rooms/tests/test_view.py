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
        cls.superuser_data = {
            "email": "super@super.com",
            "first_name": "super",
            "last_name": "super",
            "age": 22,
            "password": "abc123456",
        }

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

        cls.movie_data = {
            "title": "Thor, Amor e Trovão",
            "duration": 119,
            "synopsis": "Nunca imaginei que no final eu me Thornaria um pato",
            "premiere": "2022-07-11",
            "videos": [
                {
                    "title": "Trailer Thor 1",
                    "url": "https://www.youtube.com/watch?v=sklZyTp_wwY",
                },
            ],
            "genres": [{"name": "Trovão"}, {"name": "Trovoada"}, {"name": "Martelo"}],
            "age_group": {"minimum_age": 18, "content": "Brutalidade, Steve Magau"},
            "distributor": {"name": "Wall Thisney"},
            "director": {"name": "Thiago"},
            "stars": [
                {"person": {"name": "Thiago Montserrat"}},
                {"person": {"name": "Steve Magau"}},
            ],
        }
        cls.cinema_data = {
            "name": "Cine Asno",
            "address": {
                "street": "Rua A",
                "number": "34",
                "details": "Perto da coxinharia do thiago",
                "city": {"name": "Jubileu do sul"},
                "state": {"name": "MG"},
                "country": {"name": "Brazil"},
                "district": {"name": "Guadalupe"},
            },
            "rooms": [
                {
                    "name": "SALA X",
                    "seat_rows": [8, 9, 10, 10, 10, 8, 9, 9, 10],
                    "corridors": [
                        {"column": 1, "from_row": 4, "to_row": 4},
                        {"column": 4, "from_row": 2, "to_row": 4},
                        {"column": 8, "from_row": 2, "to_row": 4},
                    ],
                }
            ],
        }

        cls.movie_session_data = {
            "price": 21.50,
            "session_datetime": "2022-09-12 11:30",
            "subtitled": True,
            "is_3d": True,
            "on_sale": False,
        }

        cls.ticket_data = {
            "session_seats": [{"seat": {"name": "A1"}}, {"seat": {"name": "A2"}}]
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
        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

    def setUp(self):
        response = self.client.post(
            "/sessions/token/",
            {"email": "super@super.com", "password": "abc123456"},
            "json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

        self.movie = self.client.post("/movies/", self.movie_data, format="json")

        response_manager = self.client.post(
            "/sessions/token/",
            {"email": "teste2@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response_manager.json()['access']}"
        )

        self.cinema = self.client.post("/cinemas/", self.cinema_data, format="json")
        self.room = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/',
            self.room_data,
            format="json",
        )
        self.movie_session = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )

        response = self.client.post(
            "/sessions/token/",
            {"email": "teste2@teste.com", "password": "1234"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

    def test_can_list_all_rooms(self):
        response = self.client.get(f"/cinemas/{self.cinema.data['id']}/")

        self.assertEqual(response.status_code, 200)

    def test_list_one_room_from_cinema(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
        )

        response = self.client.get(
            f"/cinemas/{self.cinema.data['id']}/rooms/{response.data['id']}/"
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
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
        )

        response = self.client.get(f"/cinemas/{self.cinema.data['id']}/rooms/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_manager_user_can_create_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
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
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_delete_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
        )
        response = self.client.delete(
            f"/cinemas/{self.cinema.data['id']}/rooms/{response.data['id']}/"
        )

        self.assertEqual(response.status_code, 204)

    def test_not_manager_user_cant_delete_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
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

        response = self.client.delete(
            f"/cinemas/{self.cinema.data['id']}/rooms/{room}/"
        )

        self.assertEqual(response.status_code, 403)

    def test_manager_can_update_room(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
        )
        response = self.client.patch(
            f"/cinemas/{self.cinema.data['id']}/rooms/{response.data['id']}/",
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
            f"/cinemas/{self.cinema.data['id']}/rooms/", self.room_data, "json"
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
            f"/cinemas/{self.cinema.data['id']}/rooms/{room}/",
            self.room_update,
            "json",
        )

        self.assertEqual(response.status_code, 403)

    def test_can_not_update_room_seats_if_any_seat_is_in_a_movie_session(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            self.ticket_data,
            "json",
        )

        response = self.client.patch(
            f"/cinemas/{self.cinema.data['id']}/rooms/{self.room.data['id']}/",
            self.room_update,
            "json",
        )

        self.assertEqual(response.status_code, 400)
