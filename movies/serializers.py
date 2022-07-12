from rest_framework import serializers

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


class MovieSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)
    genres = GenreSerializer(many=True)
    age_group = AgeGroupSerializer()
    distributor = DistributorSerializer()
    director = PersonSerializer()
    stars = StarSerializer(many=True)

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
        movie.genres.set(
            [Genre.objects.get_or_create(**genre_data)[0] for genre_data in genres_data]
        )

        movie.save()

        for media_data in medias_data:
            Media.objects.get_or_create(**media_data, movie=movie)

        for star_data in stars_data:
            Star.objects.get_or_create(
                person=Person.objects.get_or_create(**star_data["person"])[0],
                movie=movie,
            )

        return movie


class ListMoviesSerializer(serializers.ModelSerializer):
    medias = MediaSerializer(many=True)

    class Meta:
        model = Movie
        fields = ["id", "title", "medias"]
