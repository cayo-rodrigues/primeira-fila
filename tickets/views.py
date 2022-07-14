from django.shortcuts import render, get_object_or_404
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from utils.mixins import SerializerByMethodMixin
from rest_framework import generics
from utils.permissions import IsSuperUser, ReadOnly
from movie_sessions.models import MovieSession
from cinemas.models import Cinema

# Create your views here.

class TicketView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        cine = self.kwargs.get('cine_id')
        session = self.kwargs.get('session_id')
        get_object_or_404(MovieSession, id=session)
        get_object_or_404(Cinema, id=cine)
        serializer.save()

class TicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
