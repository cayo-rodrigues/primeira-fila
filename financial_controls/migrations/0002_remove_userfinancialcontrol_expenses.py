# Generated by Django 4.0.6 on 2022-07-18 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial_controls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userfinancialcontrol',
            name='expenses',
        ),
    ]