from django.test import TestCase
from movies.models import AgeGroup, Distributor, Genre, Media, Movie, Person

# Create your tests here.


class MovieModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.movie_data = {
            "title": "Thor: Amor e Trovão",
            "duration": 119,
            "synopsis": "O filme apresenta Thor em uma jornada diferente de tudo que ele já enfrenta...",
            "premiere": "2022-07-11",
        }
        cls.media_data = {
            "medias": [
                {
                    "name": "Trailer Thor 1",
                    "media_url": "https://www.youtube.com/watch?v=sklZyTp_wwY",
                    "is_video": True,
                },
                {
                    "name": "Poster Thor 1",
                    "media_url": "https://www.primevideo.com/detail/Catdog/0PZ0UHHQ1BN7HII88IGN6L7QE9/ref=atv_nb_lcl_fil_PH?language=fil_PH&ie=UTF8",
                    "is_video": False,
                },
            ],
        }
        cls.genres_data = {
            "genres": [{"name": "Ação"}, {"name": "Drama"}, {"name": "Trovão"}]
        }
        cls.age_group_data = {
            "age_group": {"minimum_age": 14, "content": "Uso de drogas, Thorcicolo"}
        }
        cls.distributor_data = {"distributor": {"name": "Wall Thisney"}}
        cls.director_data = {"director": {"name": "Thiago"}}
        cls.stars_data = {"stars": [{"name": "Thiago Montserrat"}, {"name": "Pão Cova"}]}

        cls.full_movie_data = {
            **cls.movie_data,
            **cls.media_data,
            **cls.genres_data,
            **cls.age_group_data,
            **cls.distributor_data,
            **cls.director_data,
            **cls.stars_data,
        }

        cls.director = Person.objects.create(**cls.director_data["director"])
        cls.distributor = Distributor.objects.create(
            **cls.distributor_data["distributor"]
        )
        cls.age_group = AgeGroup.objects.create(**cls.age_group_data["age_group"])
        cls.genre = Genre.objects.create(**cls.genres_data["genres"][0])

        cls.movie: Movie = Movie.objects.create(
            **cls.movie_data,
            director=cls.director,
            distributor=cls.distributor,
            age_group=cls.age_group
        )
        cls.movie.genres.add(cls.genre)

    def test_can_create_movie(self):
        self.assertTrue(bool(self.movie))

    def test_if_movie_has_all_fields(self):
        self.assertEqual(self.movie.title, self.movie_data["title"])
        self.assertEqual(self.movie.duration, self.movie_data["duration"])
        self.assertEqual(self.movie.premiere, self.movie_data["premiere"])
        self.assertEqual(self.movie.synopsis, self.movie_data["synopsis"])

        self.assertIs(self.movie.director, self.director)
        self.assertIs(self.movie.distributor, self.distributor)
        self.assertIs(self.movie.age_group, self.age_group)

        self.assertIn(self.genre, self.movie.genres.all())
