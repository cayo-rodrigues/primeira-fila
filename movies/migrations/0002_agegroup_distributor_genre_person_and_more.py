# Generated by Django 4.0.6 on 2022-07-12 14:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('minimum_age', models.CharField(choices=[('L', 'L'), ('10', '10'), ('12', '12'), ('14', '14'), ('16', '16'), ('18', '18')], default='L', max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.RenameModel(
            old_name='Medias',
            new_name='Media',
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='movies.movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='movies.person')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='age_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies', to='movies.agegroup'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movies', to='movies.person'),
        ),
        migrations.AddField(
            model_name='movie',
            name='distributor',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='movies.distributor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.genre'),
        ),
    ]
