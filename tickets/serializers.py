from django.shortcuts import get_object_or_404
from movie_sessions.models import SessionSeat
from movie_sessions.serializers import MovieSessionSerializer
from rest_framework import serializers
from rooms.models import Seat
from users.serializers import UserSerializer
import ipdb
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
    user = UserSerializer(read_only=True)
    movie_session = MovieSessionSerializer(read_only=True)
    session_seats = SessionSeatSerializer(many=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def create(self, validated_data: dict):
        seats = validated_data.pop("session_seats")
        ticket = Ticket.objects.create(**validated_data)

        chosen_seats = []

        for session_seat_data in seats:
            chosen_seat: SessionSeat = get_object_or_404(
                SessionSeat,
                seat=get_object_or_404(
                    Seat,
                    name=session_seat_data["seat"]["name"],
                    room=validated_data["movie_session"].room,
                ),
                is_avaliable=True,
                movie_session=validated_data["movie_session"],
            )
            chosen_seat.is_avaliable = False
            chosen_seat.save()
            chosen_seats.append(chosen_seat)

        ticket.session_seats.set(chosen_seats)
        ticket.save()

        return ticket


    def update(self, instance: Ticket, validated_data):
        # ipdb.set_trace()
        sessions_seats = validated_data.pop("session_seats")
        dado = instance.session_seats.all()
        
        for value in dado:
            value.is_avaliable = True
            value.save()

        # sessions_seats[1]["seat"] = 'E1'
        chosen_seats = []
        # ipdb.set_trace()

        if len(sessions_seats) == instance.session_seats.count():

            for session_seat_data in sessions_seats:
                # session_seat_data["seat"]["name"] = "E1"
                # ipdb.set_trace()
                session_seat_data.is_avaliable = True
                # ipdb.set_trace()
                chosen_seat: SessionSeat = get_object_or_404(
                SessionSeat,
                seat = get_object_or_404(
                    Seat,
                    name = session_seat_data["seat"]["name"],
                    room = validated_data["movie_session"].room,
                ),
                is_avaliable = True,
                movie_session = validated_data["movie_session"]
                )
                # ipdb.set_trace()
                chosen_seat.is_avaliable = False
                # ipdb.set_trace()
                chosen_seat.save()
                # ipdb.set_trace()
                chosen_seats.append(chosen_seat)
        # ipdb.set_trace()
            instance.session_seats.set(chosen_seats)
        # ipdb.set_trace()
        # instance.save()
            return instance

