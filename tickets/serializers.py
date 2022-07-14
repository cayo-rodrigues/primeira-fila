from rest_framework import serializers
from movie_sessions.serializers import MovieSessionSerializer
from rooms.serializers import RoomSerializer
from users.serializers import UserSerializer
from .models import Seat, Ticket, SessionSeat


class SeatSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    class Meta:
        model = Seat
        fields = "__all__"



class TicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie_session = MovieSessionSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


    def create(self, validated_data: dict):
        seats = validated_data.pop("seats")
        ticket = Ticket.objects.create(**validated_data)

        for session_seat_data in seats:
            SessionSeat.objects.get_or_create(
                seat=Seat.objects.get_or_create(**session_seat_data)[0],
                is_avaliable=False,
                ticket = ticket
            )
        # ticket = Ticket.objects.create(**seats)

        return ticket


class SessionSeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSeat
        fields = "__all__"

    seat = SeatSerializer()
    ticket = TicketSerializer()
    session = MovieSessionSerializer()
