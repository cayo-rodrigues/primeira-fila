# Generated by Django 4.0.6 on 2022-07-15 15:14

from django.db import migrations, models
import django.db.models.deletion
import movie_sessions.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0006_delete_sessionseat"),
        ("movie_sessions", "0002_alter_moviesession_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="moviesession",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[
                    movie_sessions.validators.ProductValidators.validate_positive
                ],
            ),
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
                        to="tickets.seat",
                    ),
                ),
                (
                    "ticket",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="session_seats",
                        to="tickets.ticket",
                    ),
                ),
            ],
        ),
    ]
