from django.test import TestCase
from users.models import User

class TestUserModel(TestCase):
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
        
        
    def test_email(self):
        user = User.objects.get(email = self.email)
        self.assertEquals(user.email, self.user.email)
        
    def test_first_name(self):
        user = User.objects.get(email = self.email)
        self.assertEquals(user.first_name, self.user.first_name)
        
    def test_is_staff(self):
        user = User.objects.get(email = self.manager_email)
        self.assertEquals(user.is_staff, True)
        
    def test_is_not_staff(self):
        user = User.objects.get(email = self.email)
        self.assertEquals(user.is_staff, False)              
        
        