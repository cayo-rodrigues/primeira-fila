# Generated by Django 4.0.6 on 2022-07-14 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("movie_sessions", "0002_alter_moviesession_price"),
        ("tickets", "0003_alter_seat_room_alter_sessionseat_movie_session_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="movie_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="movie_sessions.moviesession",
            ),
        ),
    ]
