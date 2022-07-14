# Generated by Django 4.0.6 on 2022-07-14 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0002_alter_cinema_owner'),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='cinema',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='cinemas.cinema'),
            preserve_default=False,
        ),
    ]
