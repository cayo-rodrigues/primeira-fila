# Generated by Django 4.0.6 on 2022-07-15 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_seat'),
        ('movie_sessions', '0003_alter_moviesession_price_sessionseat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionseat',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_seats', to='rooms.seat'),
        ),
    ]
