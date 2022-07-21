from cinemas.serializers import ListCinemaSerializer
from movie_sessions.models import MovieSession
from rest_framework import serializers
from utils.helpers import bulk_get_or_create

from .models import AgeGroup, Distributor, Genre, Image, Movie, Person, Star, Video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ["movie"]


class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ["movie"]


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
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
    images = MovieImageSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True)
    genres = GenreSerializer(many=True)
    stars = StarSerializer(many=True)
    movie_sessions = GeneralMovieSessionsSerializer(many=True, read_only=True)
    age_group = AgeGroupSerializer()
    distributor = DistributorSerializer()
    director = PersonSerializer()

    class Meta:
        model = Movie
        fields = "__all__"

    def create(self, validated_data: dict) -> Movie:
        director, _ = Person.objects.get_or_create(**validated_data.pop("director"))
        dist, _ = Distributor.objects.get_or_create(**validated_data.pop("distributor"))
        age_group, _ = AgeGroup.objects.get_or_create(**validated_data.pop("age_group"))

        genres_data = validated_data.pop("genres")
        stars_data = validated_data.pop("stars")
        videos_data = validated_data.pop("videos")

        movie: Movie = Movie.objects.get_or_create(
            **validated_data,
            director=director,
            distributor=dist,
            age_group=age_group,
        )[0]
        movie.set_normalized_genres(genres_data)
        movie.save()

        bulk_get_or_create(Video, videos_data, movie=movie)
        bulk_get_or_create(Star, stars_data, [("person", Person)], movie=movie)

        return movie

    def update(self, instance: Movie, validated_data: dict):
        director = validated_data.pop("director", None)
        distributor = validated_data.pop("distributor", None)
        age_group = validated_data.pop("age_group", None)

        genres = validated_data.pop("genres", None)
        stars = validated_data.pop("stars", None)
        videos = validated_data.pop("videos", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if director:
            instance.director = Person.objects.get_or_create(**director)[0]
        if distributor:
            instance.distributor = Distributor.objects.get_or_create(**distributor)[0]
        if age_group:
            instance.age_group = AgeGroup.objects.get_or_create(**age_group)[0]

        if videos:
            bulk_get_or_create(Video, videos, movie=instance)
        if stars:
            bulk_get_or_create(Star, stars, [("person", Person)], movie=instance)
        if genres:
            instance.set_normalized_genres(genres)

        instance.save()
        return instance


class ListMoviesSerializer(serializers.ModelSerializer):
    images = MovieImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    movie_sessions = GeneralMovieSessionsSerializer(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "images", "videos", "movie_sessions"]
