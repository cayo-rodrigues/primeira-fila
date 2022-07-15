from cinemas.serializers import ListCinemaSerializer
from movie_sessions.models import MovieSession
from rest_framework import serializers
from utils.helpers import bulk_get_or_create

from .models import AgeGroup, Distributor, Genre, Media, Movie, Person, Star


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ["movie"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = "__all__"


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = "__all__"


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = "__all__"


class StarSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = Star
        fields = ["person"]


class GeneralMovieSessionsSerializer(serializers.ModelSerializer):
    cinema = ListCinemaSerializer()

    class Meta:
        model = MovieSession
        fields = ["id", "session_datetime", "cinema"]


class MovieSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)
    genres = GenreSerializer(many=True)
    age_group = AgeGroupSerializer()
    distributor = DistributorSerializer()
    director = PersonSerializer()
    stars = StarSerializer(many=True)
    movie_sessions = GeneralMovieSessionsSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def create(self, validated_data: dict) -> Movie:
        director, _ = Person.objects.get_or_create(**validated_data.pop("director"))
        distributor, _ = Distributor.objects.get_or_create(
            **validated_data.pop("distributor")
        )
        age_group, _ = AgeGroup.objects.get_or_create(**validated_data.pop("age_group"))

        genres_data = validated_data.pop("genres")
        medias_data = validated_data.pop("medias")
        stars_data = validated_data.pop("stars")

        movie: Movie = Movie.objects.get_or_create(
            **validated_data,
            director=director,
            distributor=distributor,
            age_group=age_group
        )[0]
        movie.genres.set(bulk_get_or_create(Genre, genres_data))
        movie.save()

        bulk_get_or_create(Media, medias_data, movie=movie)
        bulk_get_or_create(Star, stars_data, [("person", Person)], movie=movie)

        return movie

    def update(self, instance: Movie, validated_data: dict):
        director = validated_data.pop("director", None)
        distributor = validated_data.pop("distributor", None)
        age_group = validated_data.pop("age_group", None)

        genres = validated_data.pop("genres", None)
        medias = validated_data.pop("medias", None)
        stars = validated_data.pop("stars", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if director:
            instance.director = Person.objects.get_or_create(**director)[0]
        if distributor:
            instance.distributor = Distributor.objects.get_or_create(**distributor)[0]
        if age_group:
            instance.age_group = AgeGroup.objects.get_or_create(**age_group)[0]

        if genres:
            instance.genres.set(bulk_get_or_create(Genre, genres))
        if medias:
            bulk_get_or_create(Media, medias, movie=instance)
        if stars:
            bulk_get_or_create(Star, stars, [("person", Person)], movie=instance)

        instance.save()
        return instance


class ListMoviesSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)
    movie_sessions = GeneralMovieSessionsSerializer(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "medias", "movie_sessions"]
