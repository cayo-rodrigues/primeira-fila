from rest_framework import serializers
from .models import MovieSession


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        read_only_fields = ["id", "cinema_id", "room_id", "movie_id"]
