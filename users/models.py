import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.user_manager import CustomUserManager

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
