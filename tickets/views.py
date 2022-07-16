from cinemas.models import Cinema
from movie_sessions.models import MovieSession, SessionSeat
from utils.mixins import SerializerByMethodMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.permissions import IsSuperUser, OnlySelfManagerPermission, ReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import generics

from tickets.models import Ticket
from tickets.serializers import TicketSerializer

# Create your views here.


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        cine = get_object_or_404(Cinema, id=self.kwargs.get("cine_id"))
        session = get_object_or_404(
            MovieSession, id=self.kwargs.get("session_id"), room__cinema=cine
        )
        serializer.save(movie_session=session, user=self.request.user)


class TicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = "ticket_id"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs["ticket_id"]

        get_object_or_404(Ticket, id=ticket_id)

        return Ticket.objects.all()


class TicketSessionMovieDetailsView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_id"
    
    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]
        session_id = self.kwargs["session_id"]
        ticket_id = self.kwargs["ticket_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(MovieSession, id=session_id)

        ticket = Ticket.objects.filter(
        session_id = ticket_id
        )
        return ticket

class TicketSessionMovieOneDetailsView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_id"

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]
        session_id = self.kwargs["session_id"]
        ticket_id = self.kwargs["ticket_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(MovieSession, id=session_id)

        ticket = Ticket.objects.filter(
            id= ticket_id
        )

        return ticket


