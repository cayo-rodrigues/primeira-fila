from movies.serializers import ListMoviesSerializer, MovieSerializer
from movies.tests import util
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

# Create your tests here.


class MovieViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.movie_data = util.DEFAULT_MOVIE_DATA
        cls.media_data = util.DEFAULT_MEDIAS_DATA
        cls.genres_data = util.DEFAULT_GENRES_DATA
        cls.age_group_data = util.DEFAULT_AGE_GROUP_DATA
        cls.distributor_data = util.DEFAULT_DISTRIBUTOR_DATA
        cls.director_data = util.DEFAULT_DIRECTOR_DATA
        cls.stars_data = util.DEFAULT_STARS_DATA

        cls.request_data = {
            **cls.movie_data,
            "medias": cls.media_data,
            "genres": cls.genres_data,
            "age_group": cls.age_group_data,
            "distributor": cls.distributor_data,
            "director": cls.director_data,
            "stars": cls.stars_data,
        }

        cls.super_credentials = {
            "email": "super@super.com",
            "first_name": "super",
            "last_name": "super",
            "age": 22,
            "password": "abc123456",
        }
        cls.superuser = User.objects.create_superuser(**cls.super_credentials)

        cls.manager_credentials = {
            "email": "manager@manager.com",
            "first_name": "manager",
            "last_name": "manager",
            "age": 99,
            "password": "abc123456",
            "is_staff": True,
        }
        cls.manager = User.objects.create(**cls.manager_credentials)

        serializer = MovieSerializer(
            data={**cls.request_data, "title": "Thorta, Amor e Torta"}
        )
        if serializer.is_valid():
            cls.movie = serializer.save()

    def setUp(self) -> None:
        response = self.client.post("/sessions/token/", self.super_credentials, "json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

    def test_create_movie_route_success(self):
        response = self.client.post("/movies/", self.request_data, "json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        serializer = MovieSerializer(data={**response.json(), "title": "Oto Título"})
        self.assertTrue(serializer.is_valid())

    def test_create_movie_route_wrong_data(self):
        wrong_data = {**self.request_data}
        wrong_data.pop("genres")
        wrong_data.pop("duration")

        response = self.client.post("/movies/", wrong_data, "json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_superuser_can_create_movie(self):
        response = self.client.post("/sessions/token/", self.manager_credentials, "json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

        response = self.client.post("/movies/", self.request_data, "json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_movies_route(self):
        response = self.client.get("/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("count", response.json())
        self.assertIn("next", response.json())
        self.assertIn("previous", response.json())

        movies_list = response.json()["results"]
        movies_list[0] = {**movies_list[0], "title": "Oto Título"}
        serializer = ListMoviesSerializer(data=movies_list, many=True)

        self.assertTrue(serializer.is_valid())

    def test_retrieve_movies_route(self):
        response = self.client.get(f"/movies/{self.movie.id}/")
        serializer = MovieSerializer(data={**response.json(), "title": "Oto Título"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(serializer.is_valid())

    def test_delete_movies_route(self):
        response = self.client.delete(f"/movies/{self.movie.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_movies_route(self):
        response = self.client.patch(
            f"/movies/{self.movie.id}/",
            {
                "director": {"name": "L"},
                "title": "L >>> N",
                "genres": [{"name": "Suspense"}, {"name": "Intelectual"}],
            },
            "json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MovieSerializer(data={**response.json(), "title": "Oto Título"})
        self.assertTrue(serializer.is_valid())
