from uuid import uuid4

from django.db import models
from utils.helpers import normalize_text

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

    def set_normalized_genres(self, genres_data: list[dict]):
        genres = []

        for genre in genres_data:
            genre["name"] = normalize_text(genre["name"], is_lower=True)
            existing_genre = Genre.objects.filter(name=genre["name"]).first()
            if existing_genre:
                genres.append(existing_genre)
            else:
                genres.append(Genre.objects.create(**genre))

        self.genres.set(genres)

    def save(self, *args, **kwargs) -> None:
        self.title = normalize_text(self.title, is_title=True)
        return super().save(*args, **kwargs)


class Media(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)
    media_url = models.URLField()
    is_video = models.BooleanField(default=False)

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="medias")


class Person(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)

    def save(self, *args, **kwargs) -> None:
        self.name = normalize_text(self.name, is_lower=True)
        return super().save(*args, **kwargs)


class Star(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="stars")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="stars")


class Distributor(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)

    def save(self, *args, **kwargs) -> None:
        self.name = normalize_text(self.name, is_lower=True)
        return super().save(*args, **kwargs)


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=127)


class AgeGroupChoices(models.IntegerChoices):
    L = 0
    TEN = 10
    TWELVE = 12
    FOURTEEN = 14
    SIXTEEN = 16
    EIGHTEEN = 18


class AgeGroup(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    minimum_age = models.IntegerField(
        choices=AgeGroupChoices.choices, default=AgeGroupChoices.L
    )
    content = models.CharField(max_length=127)

    def save(self, *args, **kwargs) -> None:
        self.content = normalize_text(self.content, is_lower=True)
        return super().save(*args, **kwargs)
