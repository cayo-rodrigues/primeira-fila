import uuid

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from utils.user_manager import CustomUserManager

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    age = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = None
    date_joined = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "age"]
    objects = CustomUserManager()

    def send_confirmation_email(self, request):
        current_host = request.get_host()

        send_mail(
            subject="Confirmação de conta no site Primeira Fila",
            message="",
            html_message=f"<h2>Olá, {self.first_name}! Muito obrigado por usar o Primeira Fila.</h2>"
            "<h3>Clique no link a seguir para ativar sua conta:</h3>"
            f"<p>{current_host}/users/accounts/{self.account_confirmation.id}/</p>"
            "<p>Atenciosamente, equipe Primeira Fila :)</p>",
            from_email=EMAIL_HOST_USER,
            recipient_list=[self.email],
            fail_silently=False,
        )


class AccountConfirmation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account_confirmation"
    )
