# Generated by Django 4.0.6 on 2022-07-19 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_accountconfirmation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountconfirmation',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account_confirmation', to=settings.AUTH_USER_MODEL),
        ),
    ]
