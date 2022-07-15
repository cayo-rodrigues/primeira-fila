from movie_sessions.serializers import MovieSessionSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Seat, SessionSeat, Ticket


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["name"]


class SessionSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSeat
        exclude = ["ticket"]
        read_only_fields = ["movie_session"]

    seat = SeatSerializer()


class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie_session = MovieSessionSerializer(read_only=True)
    session_seats = SessionSeatSerializer(many=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validated_data: dict):
        seats = validated_data.pop("session_seats")
        ticket = Ticket.objects.create(**validated_data)

        for session_seat_data in seats:
            SessionSeat.objects.create(
                seat=Seat.objects.create(
                    name=session_seat_data["seat"]["name"],
                    room=validated_data["movie_session"].room,
                ),
                is_avaliable=False,
                movie_session=validated_data["movie_session"],
                ticket=ticket,
            )

        return ticket
