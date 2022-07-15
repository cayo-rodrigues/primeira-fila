from django.test import TestCase
from movie_sessions.models import MovieSession
from cinemas.models import Cinema
from rooms.models import Room
from movies.models import Movie, Person, Distributor, Star, Genre, AgeGroup, Media
from users.models import User


class MovieSessionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(
            email="gerente@email.com",
            first_name="Gerente",
            last_name="da Silva",
            age=40,
            password="abc123456",
            is_staff=True,
        )

        cls.superuser = User.objects.create_superuser(
            email="super@super.com",
            first_name="super",
            last_name="super",
            age=22,
            password="abc123456",
        )

        cls.director = Person.objects.create(name="Thiago")

        person1 = Person.objects.create(name="Steve Magau")

        genre1 = Genre.objects.create(name="Ação")

        genre2 = Genre.objects.create(name="Drama")

        genre3 = Genre.objects.create(name="Trovão")

        age_group1 = AgeGroup.objects.create(
            minimum_age=14, content="Uso de drogas, Thorcicolo"
        )

        distributor1 = Distributor.objects.create(name="Wall Thisney")

        cls.movie = Movie.objects.create(
            title="Thor: Amor e Trovão",
            duration=119,
            synopsis="O filme apresenta Thor em uma jornada diferente de tudo que ele já enfrenta...",
            premiere="2022-07-11",
            genres=[genre1, genre2, genre3],
            age_group=age_group1,
            distributor=distributor1,
            director=cls.director,
        )

        cls.media1 = Media.objects.create(
            name="Trailer Thor 1",
            media_url="https://wwww.video.com",
            is_video=True,
            movie=cls.movie,
        )
                
        cls.media2 = Media.objects.create(
            name="Poster Thor 1",
            media_url="https://wwww.imagem.com",
            is_video=False,
            movie=cls.movie,
        ),

        cls.star1 = Star.objects.create(person=cls.director, movie=cls.movie)

        cls.star2 = Star.objects.create(person=person1, movie=cls.movie)

        cls.cinema = Cinema.objects.create(
            name="Cine Asno",
            address={
                "street": "Rua A",
                "number": "34",
                "details": "Perto da coxinharia do thiago",
                "city": {"name": "Jubileu do sul"},
                "state": {"name": "MG"},
                "country": {"name": "Brazil"},
                "district": {"name": "Guadalupe"},
            },
            rooms=[
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
        )

        cls.room = Room.objects.create(
            name="SALA ADA",
            seat_rows=[
                {"row": "A", "seat_count": 10},
                {"row": "B", "seat_count": 8},
                {"row": "C", "seat_count": 8},
                {"row": "D", "seat_count": 8},
                {"row": "E", "seat_count": 8},
                {"row": "F", "seat_count": 8},
                {"row": "G", "seat_count": 8},
            ],
            room_corridors=[
                {"column": 1, "from_row": 2, "to_row": 7},
                {"column": 8, "from_row": 2, "to_row": 7},
            ],
            cinema=cls.cinema,
        )

        cls.movie_session = MovieSession.objects.create(
            price=21.50,
            session_datetime="2002-07-11 11:30",
            subtitled=True,
            is_3d=True,
            on_sale=False,
            cinema=cls.cinema,
            room=cls.room,
            movie=cls.movie,
        )

    def test_price_max_digits(self):
        movie_session = self.movie_session
        max_digits = movie_session._meta.get_field("price").max_digits
        self.assertEquals(max_digits, 10)
