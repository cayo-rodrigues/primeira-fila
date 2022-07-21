from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.email = "ordinary_user@gmail.com"
        self.password = "123Abestado4"
        self.first_name = "Ari"
        self.last_name = "Aqui"
        self.age = 12

        self.user = User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            age=self.age,
        )

    def test_can_create_an_user(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }
        response = self.client.post("/users/", user, format="json")
        self.assertEqual(response.json()["is_staff"], False)
        self.assertEqual(response.status_code, 201)

    def test_can_create_a_manager(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 30,
            "is_staff": True,
        }
        response = self.client.post("/users/", user, format="json")
        self.assertEqual(response.json()["is_staff"], True)
        self.assertEqual(response.status_code, 201)

    def test_cannot_create_user_with_repeated_email(self):
        user = {
            "email": self.email,
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }
        response = self.client.post("/users/", user, format="json")
        self.assertEquals(
            response.data, {"email": ["user with this email already exists."]}
        )
        self.assertEqual(response.status_code, 400)

    def test_can_show_self_user(self):
        user_data = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }

        user = User.objects.create(**user_data)
        user.is_active = True
        user.save()

        token = self.client.post(
            "/sessions/token/",
            {"email": "aaa@mail.com", "password": "123456"},
            format="json",
        ).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        response = self.client.get("/users/self/")
        self.assertEqual(response.status_code, 200)

    def test_can_update_self_user(self):
        user_data = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }

        user = User.objects.create(**user_data)
        user.is_active = True
        user.save()

        data = {"first_name": "Anderson"}

        token = self.client.post(
            "/sessions/token/",
            {"email": "aaa@mail.com", "password": "123456"},
            format="json",
        ).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.patch("/users/self/", data, format="json")
        self.assertEqual(response.json()["first_name"], "Anderson")
        self.assertEqual(response.status_code, 200)

    def test_can_delete_self_user(self):
        user_data = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456",
            "age": 14,
        }
        user = User.objects.create(**user_data)
        user.is_active = True
        user.save()

        token = self.client.post(
            "/sessions/token/",
            {"email": "aaa@mail.com", "password": "123456"},
            format="json",
        ).json()["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        response = self.client.delete("/users/self/")
        self.assertEqual(response.status_code, 204)


class TestUserLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.invalid_data = {"email": "abc@abc.com"}
        cls.login_data = {"email": "user@user.com", "password": "1234"}
        cls.valid_data = {
            "first_name": "user",
            "last_name": "user",
            "age": 12,
            **cls.login_data,
        }
        cls.refre_data = {"username": "jd", "password": "1234"}

        cls.user = User.objects.create(**cls.valid_data)
        cls.user.is_active = True
        cls.user.save()

    def test_login_sucess(self):
        res = self.client.post("/sessions/token/", data=self.login_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_invalid_credentials(self):
        res = self.client.post(
            "/sessions/token/", data=self.invalid_data, format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_sucess(self):
        res = self.client.post("/sessions/token/", data=self.login_data, format="json")
        refre = self.client.post(
            "/sessions/token/refresh/",
            data={"refresh": res.data["refresh"]},
            format="json",
        )
        self.assertEqual(refre.status_code, status.HTTP_200_OK)
        self.assertIn("access", refre.data)
        self.assertIn("refresh", refre.data)

    def test_refresh_invalid_credentials(self):
        refre = self.client.post(
            "/sessions/token/refresh/",
            data={"refresh": "fsdfsdf4sd65f465sd4f4sd65f"},
            format="json",
        )
        self.assertEqual(refre.status_code, status.HTTP_401_UNAUTHORIZED)
