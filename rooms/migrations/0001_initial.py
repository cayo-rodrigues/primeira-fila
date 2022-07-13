# Generated by Django 4.0.6 on 2022-07-12 22:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SeatRows',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('row', models.CharField(max_length=50)),
                ('seat_count', models.IntegerField()),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seats_room', to='rooms.room')),
            ],
        ),
        migrations.CreateModel(
            name='RoomCorridor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('column', models.IntegerField()),
                ('from_row', models.IntegerField()),
                ('to_row', models.IntegerField()),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corridors_room', to='rooms.room')),
            ],
        ),
    ]
