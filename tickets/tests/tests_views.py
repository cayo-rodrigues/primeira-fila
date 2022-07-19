from rest_framework.test import APITestCase
from django.db import IntegrityError
from users.models import User


class TicketViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.manager_data = {
            "email": "gerente@email.com",
            "first_name": "Gerente",
            "last_name": "da Silva",
            "age": 40,
            "password": "abc123456",
            "is_staff": True,
        }
        cls.normal_user_data = {
            "email": "user@teste.com",
            "first_name": "Não Gerente",
            "last_name": "da Silva",
            "age": 40,
            "password": "12345678",
        }
        cls.superuser_data = {
            "email": "super@super.com",
            "first_name": "super",
            "last_name": "super",
            "age": 22,
            "password": "abc123456",
        }
        cls.movie_data = {
            "title": "Thor, Amor e Trovão",
            "duration": 119,
            "synopsis": "Nunca imaginei que no final eu me Thornaria um pato",
            "premiere": "2022-07-11",
            "medias": [
                {
                    "name": "Poster Telescópio 1",
                    "media_url": "https://ultimosegundo.ig.com.br/ciencia/2022-07-11/primeira-foto-do-james-webb-mostra-galaxias-pouco-apos-o-big-bang.html",
                    "is_video": False,
                }
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
        cls.room_data = {
            "name": "SALA ADA",
            "seat_rows": [
                {"row": "A", "seat_count": 10},
                {"row": "B", "seat_count": 8},
                {"row": "C", "seat_count": 8},
                {"row": "D", "seat_count": 8},
                {"row": "E", "seat_count": 8},
                {"row": "F", "seat_count": 8},
                {"row": "G", "seat_count": 8},
            ],
            "room_corridors": [
                {"column": 1, "from_row": 2, "to_row": 7},
                {"column": 8, "from_row": 2, "to_row": 7},
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
            "session_seats": [{"seat": {"name": "A8"}}, {"seat": {"name": "A9"}}]
        }

        cls.superuser = User.objects.create_superuser(**cls.superuser_data)
        cls.normal_user = User.objects.create(**cls.normal_user_data)
        cls.normal_user.is_active = True
        cls.normal_user.save()

    def setUp(self):
        response = self.client.post(
            "/sessions/token/",
            {"email": "super@super.com", "password": "abc123456"},
            "json",
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )
        self.movie = self.client.post("/movies/", self.movie_data, format="json")

        self.manager = User.objects.create(**self.manager_data)
        self.manager.is_active = True
        self.manager.save()

        response_manager = self.client.post(
            "/sessions/token/",
            {"email": "gerente@email.com", "password": "abc123456"},
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
            {"email": "user@teste.com", "password": "12345678"},
            "json",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}"
        )

    def test_can_create_a_ticket(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            self.ticket_data,
            "json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["id"])

    def test_all_valid_fields(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            self.ticket_data,
            "json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data["total"])
        self.assertIsNotNone(response.data["user"])
        self.assertIsNotNone(response.data["movie_session"])

    def test_can_not_create_ticket_with_ocupied_seat(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            self.ticket_data,
            "json",
        )

        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            self.ticket_data,
            "json",
        )

        self.assertEqual(response.status_code, 404)

    def test_can_not_create_ticket_with_unknown_seat(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            {"session_seats": [{"seat": {"name": "A211"}}]},
            "json",
        )

        self.assertEqual(response.status_code, 404)

    def test_invalid_request_field(self):
        response = self.client.post(
            f"/cinemas/{self.cinema.data['id']}/movie-sessions/{self.movie_session.data['id']}/tickets/",
            {},
            "json",
        )

        self.assertEqual(response.status_code, 400)
