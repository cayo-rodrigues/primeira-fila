from django.test import TestCase
from users.models import User

class TestUserView(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        self.email = "ordinary_user@gmail.com"
        self.manager_email = "gerente@gmail.com"
        self.password = "123Abestado4"
        self.first_name = "Ari"
        self.last_name = "Aqui"
        self.age = 12
        self.user = User.objects.create_user(email=self.email, password=self.password, first_name=self.first_name, last_name=self.last_name, age=self.age)
        self.user_manager = User.objects.create_user(email=self.manager_email, password=self.password, first_name="Gerente", last_name="da Silva", age=40, is_staff=True)
     
        
    def test_can_create_an_user(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456"
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
            "is_staff":True
        }
        response = self.client.post("/users/", user, format="json")
        self.assertEqual(response.json()["is_staff"], True)
        self.assertEqual(response.status_code, 201)
     
        
    def test_cannot_create_user_with_repeated_email(self):
        user = {
            "email": self.email,
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456"
        }
        response = self.client.post("/users/", user, format="json")
        self.assertEquals(response.data,{
            "email": [
                "user with this email already exists."
            ]
        }) 
        self.assertEqual(response.status_code, 400)   
     
        
    def test_can_show_self_user(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456"
        }
        self.client.post("/users/", user, format="json")
        response = self.client.get("/users/self/")
        self.assertEqual(response.status_code, 200)
        
        
    def test_can_update_self_user(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456"
        }
        data = {
            "first_name":"Anderson"
        }
        self.client.post("/users/", user, format="json")
        response = self.client.patch("/users/self/", data, format="json")
        self.assertEqual(response.json()["first_name"], "Anderson")
        self.assertEqual(response.status_code, 200)
        
        
    def test_can_delete_self_user(self):
        user = {
            "email": "aaa@mail.com",
            "first_name": "A",
            "last_name": "Da Silva",
            "password": "123456"
        }
        self.client.post("/users/", user, format="json") 
        response = self.client.delete("/users/self/")   
        self.assertEqual(response.status_code, 204)               