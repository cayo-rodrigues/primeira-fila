
from email.headerregistry import Address
from django.test import TestCase
from movie_sessions.models import MovieSession
from cinemas.models import Cinema
from rooms.models import Room, RoomCorridor, SeatRows
from movies.models import Movie, Person, Distributor, Star, Genre, AgeGroup, Media
from users.models import User
from addresses.models import Address, District, City, Country, State
from django.utils import timezone
from django.core.exceptions import ValidationError

import ipdb

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
            premiere=timezone.now(),
            age_group=age_group1,
            distributor=distributor1,
            director=cls.director,
        )

        genres = [genre1, genre2, genre3]

        for value in genres:
            cls.movie.genres.add(value)

        cls.media1 = Media.objects.create(
            name="Trailer Thor 1",
            media_url="https://wwww.video.com",
            is_video=True,
            movie=cls.movie,
        )

        cls.media2 = (
            Media.objects.create(
                name="Poster Thor 1",
                media_url="https://wwww.imagem.com",
                is_video=False,
                movie=cls.movie,
            ),
        )

        cls.star1 = Star.objects.create(person=cls.director, movie=cls.movie)

        cls.star2 = Star.objects.create(person=person1, movie=cls.movie)

        district = District.objects.create(name="Guadalupe")
        city = City.objects.create(name="Jubileu do Sul")
        state = State.objects.create(name="MG")
        country = Country.objects.create(name="Brazil")

        address = Address.objects.create(
            street="Rua A",
            number="34",
            details="Perto da coxinharia do thiago",
            district=district,
            city=city,
            state=state,
            country=country,
        )

        seat_row1 = SeatRows.objects.create(row="A", seat_count=10)
        seat_row2 = SeatRows.objects.create(row="B", seat_count=8)
        seat_row3 = SeatRows.objects.create(row="C", seat_count=8)

        room_corridor1 = RoomCorridor.objects.create(column=1, from_row=2, to_row=7)
        room_corridor2 = RoomCorridor.objects.create(column=8, from_row=2, to_row=7)

        cls.cinema = Cinema.objects.create(
            name="Cine Asno",
            owner=cls.user,
            address=address,
        )

        cls.room = Room.objects.create(
            name="SALA ADA",
            cinema=cls.cinema,
        )

        seat_rows = [seat_row1, seat_row2, seat_row3]
        for value in seat_rows:
            cls.room.seat_rows.add(value)

        room_corridors=[room_corridor1, room_corridor2]
        for value in room_corridors:
            cls.room.room_corridors.add(value)    


        cls.movie_session = MovieSession.objects.create(
            price=21.50,
            session_datetime=timezone.now(),
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

    def test_price_cannot_be_a_negative_value(self):
        with self.assertRaises(ValidationError):
            movie_session = MovieSession.objects.create(
                price=-21.50,
                session_datetime=timezone.now(),
                subtitled=True,
                is_3d=True,
                on_sale=False,
                cinema=self.cinema,
                room=self.room,
                movie=self.movie,
            )

            movie_session.full_clean()




