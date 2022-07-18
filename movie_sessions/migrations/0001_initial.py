# Generated by Django 4.0.6 on 2022-07-17 23:52

from django.db import migrations, models
import django.db.models.deletion
import movie_sessions.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            movie_sessions.validators.PriceValidators.validate_positive
                        ],
                    ),
                ),
                ("session_datetime", models.DateTimeField()),
                ("subtitled", models.BooleanField()),
                ("is_3d", models.BooleanField()),
                ("on_sale", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="SessionSeat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("is_avaliable", models.BooleanField(default=True)),
                (
                    "movie_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_seats",
                        to="movie_sessions.moviesession",
                    ),
                ),
                (
                    "seat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_seats",
                        to="rooms.seat",
                    ),
                ),
            ],
        ),
    ]
