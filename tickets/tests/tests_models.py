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
from django.test import TestCase
from django.utils import timezone
from movie_sessions.models import MovieSession
from movies.models import AgeGroup, Distributor, Genre, Image, Movie, Person, Star, Video
from rooms.models import Room, RoomCorridor, SeatRow
from tickets.models import Ticket
from users.models import User


class TicketModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create(
            email="teste@teste.com",
            password="1234",
            first_name="Teste",
            last_name="Teste",
            age=40,
        )

        cls.room_name = "Sala 1"
        cls.row = "A"
        cls.seats_count = 10

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

        cls.superuser = User.objects.create_superuser(
            email="super@super.com",
            first_name="super",
            last_name="super",
            age=22,
            password="abc123456",
        )

        cls.director = Person.objects.create(name="Thiago")

        cls.person1 = Person.objects.create(name="Steve Magau")

        cls.genre1 = Genre.objects.create(name="Ação")

        cls.genre2 = Genre.objects.create(name="Drama")

        cls.genre3 = Genre.objects.create(name="Trovão")

        cls.age_group1 = AgeGroup.objects.create(
            minimum_age=14, content="Uso de drogas, Thorcicolo"
        )

        cls.distributor1 = Distributor.objects.create(name="Wall Thisney")

        cls.movie = Movie.objects.create(
            title="Thor: Amor e Trovão",
            duration=119,
            synopsis="O filme apresenta Thor em uma jornada diferente de tudo que ele já enfrenta...",
            premiere=timezone.now(),
            age_group=cls.age_group1,
            distributor=cls.distributor1,
            director=cls.director,
        )

        cls.genres = [cls.genre1, cls.genre2, cls.genre3]

        for value in cls.genres:
            cls.movie.genres.add(value)

        cls.media1 = Video.objects.create(
            title="Trailer Thor 1",
            url="https://wwww.video.com",
            movie=cls.movie,
        )

        cls.media2 = (
            Image.objects.create(
                title="Poster Thor 1",
                file="https://wwww.imagem.com",
                movie=cls.movie,
            ),
        )

        cls.star1 = Star.objects.create(person=cls.director, movie=cls.movie)

        cls.star2 = Star.objects.create(person=cls.person1, movie=cls.movie)

        district = District.objects.create(name="Guadalupe")
        city = City.objects.create(name="Jubileu do Sul")
        state = State.objects.create(name="MG")
        country = Country.objects.create(name="Brazil")

        cls.address = Address.objects.create(
            street="Rua A",
            number="34",
            details="Perto da coxinharia do thiago",
            district=district,
            city=city,
            state=state,
            country=country,
        )

        seat_row1 = SeatRow.objects.create(row="A", seat_count=10)
        seat_row2 = SeatRow.objects.create(row="B", seat_count=8)
        seat_row3 = SeatRow.objects.create(row="C", seat_count=8)

        room_corridor1 = RoomCorridor.objects.create(column=1, from_row=2, to_row=7)
        room_corridor2 = RoomCorridor.objects.create(column=8, from_row=2, to_row=7)

        cls.cinema = Cinema.objects.create(
            name="Cine Asno",
            owner=cls.user,
            address=cls.address,
        )

        cls.room = Room.objects.create(
            name="SALA ADA",
            cinema=cls.cinema,
        )

        seat_rows = [seat_row1, seat_row2, seat_row3]
        for value in seat_rows:
            cls.room.seat_rows.add(value)

        room_corridors = [room_corridor1, room_corridor2]
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

    def test_can_create_a_ticket(self):
        ticket = Ticket.objects.create(user=self.user, movie_session=self.movie_session)

        ticket.save()
        self.assertIsNotNone(ticket)

    def test_can_not_create_a_ticket(self):
        with self.assertRaises(ValueError):
            ticket = Ticket.objects.create(user="1", movie_session=[])

            ticket.save()

    def test_user_exist_in_ticket(self):
        ticket = Ticket.objects.create(user=self.user, movie_session=self.movie_session)

        self.assertIsNotNone(ticket.user)

    def test_movie_session_exists_in_ticket(self):
        ticket = Ticket.objects.create(user=self.user, movie_session=self.movie_session)

        self.assertIsNotNone(ticket.movie_session)
