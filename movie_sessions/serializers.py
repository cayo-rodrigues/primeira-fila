from rest_framework import serializers
from tickets.models import Seat

from .models import MovieSession, SessionSeat


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = "__all__"
        read_only_fields = ["id", "cinema", "room", "movie"]

    def create(self, validated_data: dict):
        movie_session = MovieSession.objects.create(**validated_data)

        SessionSeat.objects.bulk_create(
            [
                SessionSeat(
                    is_avaliable=True,
                    movie_session=movie_session,
                    seat=seat,
                )
                for seat in validated_data["room"].seats.all()
            ]
        )

        return movie_session
