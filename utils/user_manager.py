from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create(
        self,
        email,
        first_name,
        last_name,
        age,
        password=None,
        is_staff=False,
        **extra_fields
    ):
        now = timezone.now()

        if not email:
            raise ValueError("Must provide an email")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            age=age,
            is_staff=is_staff,
            is_active=False,
            last_login=now,
            created_at=now,
            updated_at=now,
            **extra_fields
        )
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, age, password=None, **extra_fields
    ):
        user = self.create(
            email, first_name, last_name, age, password, True, **extra_fields
        )
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user
