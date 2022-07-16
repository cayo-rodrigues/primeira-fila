# Generated by Django 4.0.6 on 2022-07-16 00:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addresses', '0004_alter_address_details_alter_address_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to='addresses.address')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cinemas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
