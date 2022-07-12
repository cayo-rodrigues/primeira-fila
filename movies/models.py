from uuid import uuid4

from django.db import models

# Create your models here.


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=127, unique=True)
    duration = models.PositiveIntegerField()
    synopsis = models.TextField()
    premiere = models.DateField()

    director = models.ForeignKey(
        "movies.Person",
        on_delete=models.SET_NULL,
        related_name="movies",
        null=True,
        blank=True,
        default=None,
    )
    distributor = models.ForeignKey(
        "movies.Distributor", on_delete=models.CASCADE, related_name="movies"
    )
    age_group = models.ForeignKey(
        "movies.AgeGroup",
        on_delete=models.SET_NULL,
        related_name="movies",
        null=True,
        blank=True,
        default=None,
    )
    genres = models.ManyToManyField("movies.Genre", related_name="movies")


class Media(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)
    media_url = models.URLField()
    is_video = models.BooleanField(default=False)

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="medias")


class Person(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)


class Star(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="stars")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="stars")


class Distributor(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)


class AgeGroupChoices(models.TextChoices):
    L = ("L", "L")
    TEN = ("10", "10")
    TWELVE = ("12", "12")
    FOURTEEN = ("14", "14")
    SIXTEEN = ("16", "16")
    EIGHTEEN = ("18", "18")


class AgeGroup(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    minimum_age = models.CharField(
        max_length=127, choices=AgeGroupChoices.choices, default=AgeGroupChoices.L
    )
    content = models.CharField(max_length=127)
