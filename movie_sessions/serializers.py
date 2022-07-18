from rest_framework import serializers


from .models import MovieSession, SessionSeat


class MovieSessionSerializer(serializers.ModelSerializer):
    available_seats_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MovieSession
        fields = "__all__"
        read_only_fields = ["id", "cinema", "room", "movie"]
        depth = 1

    def create(self, validated_data: dict):
        movie_session = MovieSession.objects.create(**validated_data)

        SessionSeat.objects.bulk_create(
            [
                SessionSeat(
                    is_available=True,
                    movie_session=movie_session,
                    seat=seat,
                )
                for seat in validated_data["room"].seats.all()
            ]
        )

        return movie_session

    def get_available_seats_count(self, movie_session: MovieSession):
        seats = movie_session.session_seats.all()
        available_seats = seats.filter(is_available=True)
        return len(available_seats)
