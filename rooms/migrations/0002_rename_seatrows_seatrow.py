# Generated by Django 4.0.6 on 2022-08-12 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SeatRows',
            new_name='SeatRow',
        ),
    ]
