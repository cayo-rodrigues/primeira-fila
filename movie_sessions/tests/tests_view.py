from rest_framework.test import APITestCase
from users.models import User


class MovieSessionViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "email": "gerente@email.com",
            "first_name": "Gerente",
            "last_name": "da Silva",
            "age": 40,
            "password": "abc123456",
            "is_staff": True,
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
            "session_datetime": "3022-07-11 11:30",
            "subtitled": True,
            "is_3d": True,
            "on_sale": False,
        }

        cls.superuser = User.objects.create_superuser(**cls.superuser_data)

    def setUp(self) -> None:
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

        self.user = User.objects.create(**self.user_data)
        self.user.is_active = True
        self.user.save()

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
            f'/cinemas/{self.cinema.data["id"]}/rooms/', self.room_data, format="json"
        )

    def test_can_create_a_movie_session(self):
        response = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_can_list_a_movie_session(self):
        session = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )
        response = self.client.get(
            f'/cinemas/{self.cinema.data["id"]}/movie-sessions/{session.data["id"]}/'
        )
        self.assertEqual(response.status_code, 200)

    def test_can_list_all_movie_sessions_from_a_cinema(self):
        self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )
        response = self.client.get(f'/cinemas/{self.cinema.data["id"]}/movie-sessions/')
        self.assertEqual(response.status_code, 200)

    def test_can_list_all_movie_sessions_from_a_movie(self):
        self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )
        response = self.client.get(
            f'/cinemas/{self.cinema.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/'
        )
        self.assertEqual(response.status_code, 200)

    def test_can_update_a_movie_session(self):
        movie_session = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )

        data = {"on_sale": True}
        response = self.client.patch(
            f'/cinemas/{self.cinema.data["id"]}/movie-sessions/{movie_session.data["id"]}/',
            data,
            format="json",
        )
        self.assertEqual(response.status_code, 200)

    def test_can_delete_a_movie_session(self):
        movie_session = self.client.post(
            f'/cinemas/{self.cinema.data["id"]}/rooms/{self.room.data["id"]}/movies/{self.movie.data["id"]}/movie-sessions/',
            self.movie_session_data,
            format="json",
        )
        response = self.client.delete(
            f'/cinemas/{self.cinema.data["id"]}/movie-sessions/{movie_session.data["id"]}/'
        )
        self.assertEqual(response.status_code, 204)
