from django.test import TestCase
from movies.models import AgeGroup, Distributor, Genre, Media, Movie, Person, Star
from movies.tests import util

# Create your tests here.


class MovieModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.movie_data = util.DEFAULT_MOVIE_DATA
        cls.media_data = util.DEFAULT_MEDIAS_DATA
        cls.genres_data = util.DEFAULT_GENRES_DATA
        cls.age_group_data = util.DEFAULT_AGE_GROUP_DATA
        cls.distributor_data = util.DEFAULT_DISTRIBUTOR_DATA
        cls.director_data = util.DEFAULT_DIRECTOR_DATA
        cls.stars_data = util.DEFAULT_STARS_DATA

        cls.director = Person.objects.create(**cls.director_data)
        cls.distributor = Distributor.objects.create(**cls.distributor_data)
        cls.age_group = AgeGroup.objects.create(**cls.age_group_data)
        cls.genre = Genre.objects.create(**cls.genres_data[0])
        cls.person = Person.objects.create(**cls.stars_data[0]["person"])

        cls.movie: Movie = Movie.objects.create(
            **cls.movie_data,
            director=cls.director,
            distributor=cls.distributor,
            age_group=cls.age_group
        )
        cls.movie.genres.add(cls.genre)

        cls.media = Media.objects.create(**cls.media_data[0], movie=cls.movie)
        cls.star = Star.objects.create(person=cls.person, movie=cls.movie)

    def test_can_create_movie(self):
        self.assertTrue(bool(self.movie))

    def test_if_movie_has_all_fields(self):
        self.assertEqual(self.movie.title, self.movie_data["title"].title())
        self.assertEqual(self.movie.duration, self.movie_data["duration"])
        self.assertEqual(self.movie.premiere, self.movie_data["premiere"])
        self.assertEqual(self.movie.synopsis, self.movie_data["synopsis"])

        self.assertIs(self.movie.director, self.director)
        self.assertIs(self.movie.distributor, self.distributor)
        self.assertIs(self.movie.age_group, self.age_group)

        self.assertIn(self.genre, self.movie.genres.all())
        self.assertIn(self.star, self.movie.stars.all())
        self.assertIn(self.media, self.movie.medias.all())
