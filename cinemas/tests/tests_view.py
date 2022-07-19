from cinemas.serializers import CreateCinemaSerializer
from cinemas.tests.util import DEFAULT_ADDRESS_FULL_DATA, DEFAULT_CINEMA_DATA
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User

# Create your tests here.


class CinemaViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cinema_data = DEFAULT_CINEMA_DATA
        cls.address_data = DEFAULT_ADDRESS_FULL_DATA

        cls.request_data = {
            **cls.cinema_data,
            "address": cls.address_data,
        }

        cls.manager_credentials = {
            "email": "manager@manager.com",
            "first_name": "manager",
            "last_name": "manager",
            "age": 99,
            "password": "abc123456",
            "is_staff": True,
        }

        cls.manager = User.objects.create(**cls.manager_credentials)
        cls.manager.is_active = True
        cls.manager.save()


        cls.user_credentials = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }

        cls.user = User.objects.create(**cls.user_credentials)
        cls.user.is_active = True
        cls.user.save()


        cls.product = {
            "description": "Descrição do produto",
            "price": 20,
            "quantity": 10,
            "is_active": True,
        }

    def setUp(self) -> None:
        response = self.client.post("/sessions/token/", self.manager_credentials, "json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")

    def test_create_cinema_route_success(self):
        response = self.client.post("/cinemas/", self.request_data, "json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        serializer = CreateCinemaSerializer(data={**response.json(), "name": "Cinemark"})
        self.assertTrue(serializer.is_valid())

    def test_create_cinema_route_wrong_data(self):
        wrong_data = {**self.request_data}
        wrong_data.pop("address")
        wrong_data.pop("name")

        response = self.client.post("/cinemas/", wrong_data, "json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_cinema_route(self):
        response = self.client.post("/cinemas/", self.request_data, format="json")

        self.client.credentials(HTTP_AUTHORIZATION="")

        response_get = self.client.get("/cinemas/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_retrieve_cinema_route(self):
        x = self.client.post(
            "/cinemas/",
            data={
                "name": "Notebook Ideapad310",
                "address": {
                    "street": "Rua A",
                    "number": "34",
                    "details": "Perto da coxinharia do thiago",
                    "city": {"name": "Jubileu do sul"},
                    "district": {"name": "Vila Nova"},
                    "state": {"name": "MG"},
                    "country": {"name": "Brazil"},
                },
            },
            format="json",
        )

        response = self.client.get(f'/cinemas/{x.data["id"]}/')

    def test_delete_cinema_route(self):
        response = self.client.post("/cinemas/", self.request_data, format="json")

        response = self.client.delete(f'/cinemas/{response.data["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_cinema_route(self):
        response = self.client.post("/cinemas/", self.request_data, format="json")

        response_patch = self.client.patch(
            f'/cinemas/{response.data["id"]}/',
            {"name": "bubu"},
            "json",
        )

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
