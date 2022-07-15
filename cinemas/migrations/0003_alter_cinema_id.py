# Generated by Django 4.0.6 on 2022-07-14 13:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cinemas', '0002_alter_cinema_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinema',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]