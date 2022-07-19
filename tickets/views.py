from cinemas.models import Cinema
from django.shortcuts import get_object_or_404
from movie_sessions.models import MovieSession
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket
from tickets.serializers import TicketSerializer

from drf_spectacular.utils import extend_schema

# Create your views here.

@extend_schema(
    operation_id="ticket_post_get",
    request=TicketSerializer,
    responses=TicketSerializer,
    description = 'Route for list/create a ticket', 
    summary='List/create ticket',
    tags=['create/list tickets']
)
class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        cine = get_object_or_404(Cinema, id=self.kwargs.get("cine_id"))
        session = get_object_or_404(
            MovieSession, id=self.kwargs.get("session_id"), room__cinema=cine
        )
        serializer.save(movie_session=session, user=self.request.user)


@extend_schema(
    operation_id="ticket_retrieve",
    request=TicketSerializer,
    responses=TicketSerializer,
    description = 'Route for list one ticket', 
    summary='Retrieve ticket',
    tags=['retrieve ticket of a user']
)
class TicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
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

        ticket = Ticket.objects.filter(session_id=ticket_id)
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

        ticket = Ticket.objects.filter(id=ticket_id)

        return ticket

@extend_schema(
    operation_id="ticket_retrieve",
    request=TicketSerializer,
    responses=TicketSerializer,
    description = 'Route for list one ticket',
    tags=['retrieve ticket of a user']
)
class TicketUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_id"

    def perform_update(self, serializer):
        cine = get_object_or_404(Cinema, id=self.kwargs.get("cine_id"))
        session = get_object_or_404(
            MovieSession, id=self.kwargs.get("session_id"), room__cinema=cine
        )
        ticket = get_object_or_404(Ticket, id=self.kwargs.get("ticket_id"))
        serializer.save(movie_session=session, user=self.request.user)
