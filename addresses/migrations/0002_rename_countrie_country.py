# Generated by Django 4.0.6 on 2022-07-12 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("addresses", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Countrie",
            new_name="Country",
        ),
    ]
