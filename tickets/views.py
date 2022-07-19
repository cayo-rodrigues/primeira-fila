from cinemas.models import Cinema
from movie_sessions.models import MovieSession
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import (
    CinemaNotFoundError,
    MovieSessionNotFoundError,
    TicketNotFoundError,
)
from utils.helpers import safe_get_object_or_404
from utils.permissions import IsTicketOwner

from tickets.models import Ticket
from tickets.serializers import TicketSerializer

# Create your views here.


class TicketView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        cine = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, id=self.kwargs.get("cine_id")
        )
        session = safe_get_object_or_404(
            MovieSession,
            MovieSessionNotFoundError,
            id=self.kwargs.get("session_id"),
            room__cinema=cine,
        )
        return serializer.save(movie_session=session, user=self.request.user)


class UserTicketDetailsView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_id"
    permission_classes = [IsAuthenticated, IsTicketOwner]


class TicketSessionMovieView(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]
        session_id = self.kwargs["session_id"]

        cinema = safe_get_object_or_404(Cinema, CinemaNotFoundError, id=cinema_id)
        session = safe_get_object_or_404(
            MovieSession, MovieSessionNotFoundError, id=session_id
        )

        return Ticket.objects.filter(movie_session=session, cinema=cinema)


class TicketSessionMovieDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_object(self):
        cinema_id = self.kwargs["cine_id"]
        session_id = self.kwargs["session_id"]
        ticket_id = self.kwargs["ticket_id"]

        cinema = safe_get_object_or_404(Cinema, CinemaNotFoundError, id=cinema_id)
        session = safe_get_object_or_404(
            MovieSession, MovieSessionNotFoundError, id=session_id
        )

        return safe_get_object_or_404(
            Ticket,
            TicketNotFoundError,
            cinema=cinema,
            movie_session=session,
            id=ticket_id,
        )


class TicketDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_id"

    def perform_update(self, serializer):
        cine = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, id=self.kwargs.get("cine_id")
        )
        session = safe_get_object_or_404(
            MovieSession,
            MovieSessionNotFoundError,
            id=self.kwargs.get("session_id"),
            room__cinema=cine,
        )
        safe_get_object_or_404(
            Ticket,
            TicketNotFoundError,
            id=self.kwargs.get("ticket_id"),
            movie_session=session,
        )
        serializer.save(movie_session=session, user=self.request.user)
