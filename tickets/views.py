from cinemas.models import Cinema
from django.shortcuts import get_object_or_404, render
from movie_sessions.models import MovieSession
from rest_framework import generics
from utils.mixins import SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly

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
