from rest_framework import serializers

from .models import AgeGroup, Distributor, Genre, Media, Movie, Person, Star


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        exclude = ["movie"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ["movies"]


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        exclude = ["movies"]


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        exclude = ["movies"]


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = ["movies", "stars"]


class MovieSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)
    genres = GenreSerializer(many=True)
    age_group = AgeGroupSerializer()
    distributor = DistributorSerializer()
    director = PersonSerializer()
    stars = PersonSerializer(many=True)

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

        movie: Movie = Movie.objects.create(
            **validated_data,
            director=director,
            distributor=distributor,
            age_group=age_group
        )
        movie.genres.set(
            [Genre.objects.get_or_create(**genre_data)[0] for genre_data in genres_data]
        )

        movie.save()

        for media_data in validated_data.pop("medias"):
            Media.objects.get_or_create(**media_data, movie=movie)

        for star_data in validated_data.pop("stars"):
            Star.objects.get_or_create(
                person=Person.objects.get_or_create(**star_data)[0], movie=movie
            )

        return movie
