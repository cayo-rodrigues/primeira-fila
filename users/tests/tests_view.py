import ipdb
from users.models import User
from rest_framework.test import APITestCase
from rest_framework.views import status


class TestUserLoginView(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.invalid_data = {
            "username": "545"
        }
        cls.valid_data = {
            "username": "th",
            "password": "1234"
        }
        cls.refre_data = {
            "username": "jd",
            "password": "1234"
        }
        
        cls.user = User.objects.create_user(**cls.valid_data)
        cls.user = User.objects.create_user(**cls.refre_data)

    def test_login_sucess(self):
        res = self.client.post("/sessions/token/", data=self.valid_data, format ="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_invalid_credentials(self):
        res = self.client.post("/sessions/token/", data=self.invalid_data, format ="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_sucess(self):
        res = self.client.post("/sessions/token/", data=self.refre_data, format ="json")
        refre = self.client.post("/sessions/token/refresh/", data={"refresh":res.data["refresh"]}, format ="json")
        self.assertEqual(refre.status_code, status.HTTP_200_OK)
        self.assertIn("access", refre.data)
        self.assertIn("refresh", refre.data)

    def test_refresh_invalid_credentials(self):
        refre = self.client.post("/sessions/token/refresh/", data={"refresh": "fsdfsdf4sd65f465sd4f4sd65f"}, format ="json")
        self.assertEqual(refre.status_code, status.HTTP_401_UNAUTHORIZED)