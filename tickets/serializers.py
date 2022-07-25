from movie_sessions.models import SessionSeat
from movie_sessions.serializers import MovieSessionSerializer
from rest_framework import serializers
from rooms.models import Seat
from users.serializers import UserSerializer
from utils.exceptions import SeatNotFoundError, SessionSeatNotFoundError
from utils.helpers import safe_get_object_or_404

from .models import Ticket


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
    total = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    movie_session = MovieSessionSerializer(read_only=True)
    session_seats = SessionSeatSerializer(many=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validated_data: dict):
        seats = validated_data.pop("session_seats")
        ticket: Ticket = Ticket.objects.create(**validated_data)
        chosen_seats = []
        for session_seat_data in seats:
            chosen_seat: SessionSeat = safe_get_object_or_404(
                SessionSeat,
                SessionSeatNotFoundError,
                seat=safe_get_object_or_404(
                    Seat,
                    SeatNotFoundError,
                    name=session_seat_data["seat"]["name"],
                    room=validated_data["movie_session"].room,
                ),
                is_available=True,
                movie_session=validated_data["movie_session"],
            )
            chosen_seat.is_available = False
            chosen_seat.save()
            chosen_seats.append(chosen_seat)
        ticket.session_seats.set(chosen_seats)
        ticket.send_by_email(self.context["request"])
        ticket.save()
        return ticket

    def get_total(self, ticket: Ticket):
        total = ticket.movie_session.price * ticket.session_seats.count()
        return total

    def update(self, instance: Ticket, validated_data):
        sessions_seats = validated_data.pop("session_seats")
        dado = instance.session_seats.all()

        for value in dado:
            value.is_available = True
            value.save()
        chosen_seats = []

        if len(sessions_seats) == instance.session_seats.count():
            for session_seat_data in sessions_seats:
                session_seat_data.is_available = True
                chosen_seat: SessionSeat = safe_get_object_or_404(
                    SessionSeat,
                    SessionSeatNotFoundError,
                    seat=safe_get_object_or_404(
                        Seat,
                        SeatNotFoundError,
                        name=session_seat_data["seat"]["name"],
                        room=instance.movie_session.room,
                    ),
                    is_available=True,
                    movie_session=instance.movie_session,
                )
                chosen_seat.is_available = False
                chosen_seat.save()
                chosen_seats.append(chosen_seat)
            instance.session_seats.set(chosen_seats)
            instance.send_by_email(self.context["request"])
            instance.save()
            return instance
