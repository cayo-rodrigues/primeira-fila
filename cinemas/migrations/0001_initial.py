# Generated by Django 4.0.6 on 2022-07-15 16:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to='addresses.address')),
            ],
        ),
    ]
