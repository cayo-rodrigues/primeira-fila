from cinemas.models import Cinema
from django.shortcuts import get_object_or_404
from movies.models import Movie
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rooms.models import Room
from utils.permissions import OwnerPermission

from .models import MovieSession
from .serializers import MovieSessionSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    operation_id="movie_session_post",
    request=MovieSessionSerializer,
    responses=MovieSessionSerializer,
    description = 'Route for register one ticket', 
    summary='Create movie session',
    tags=['create one movie session']
)
class MovieSessionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def perform_create(self, serializer):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        room = get_object_or_404(Room, pk=self.kwargs["room_id"], cinema=cinema)
        movie = get_object_or_404(Movie, pk=self.kwargs["movie_id"])

        serializer.save(cinema=cinema, room=room, movie=movie)

@extend_schema(
    operation_id="movie_session_get",
    request=MovieSessionSerializer,
    responses=MovieSessionSerializer,
    description = 'Route for list the movie sessions of a cinema', 
    summary='List movie sessions of a cinema',
    tags=['list movie sessions of a cinema']
)
class MovieSessionCinemaDetailView(generics.ListAPIView):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]

        get_object_or_404(Cinema, id=cinema_id)

        movie_sessions = MovieSession.objects.filter(cinema_id=cinema_id)

        return movie_sessions


@extend_schema(
    operation_id="movie_session_get",
    request=MovieSessionSerializer,
    responses=MovieSessionSerializer,
    description = 'Route for list the movie sessions of a movie', 
    summary='List movie sessions of a movie',
    tags=['list movie sessions of a movie']
)
class MovieSessionMovieDetailView(generics.ListAPIView):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def get_queryset(self):

        cinema_id = self.kwargs["cine_id"]
        movie_id = self.kwargs["movie_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(Movie, id=movie_id)

        movie_sessions = MovieSession.objects.filter(cinema_id=cinema_id).filter(
            movie_id=movie_id
        )

        return movie_sessions

@extend_schema(
    operation_id="movie_session_get_update_delete",
    request=MovieSessionSerializer,
    responses=MovieSessionSerializer,
    description = 'Route for list/update/delete the movie sessions of a cinema', 
    tags=['retrieve a movie session']
)
class MovieSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [OwnerPermission]
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    lookup_url_kwarg = "session_id"

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]
        movie_session_id = self.kwargs["session_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(MovieSession, id=movie_session_id)
        movie_session = MovieSession.objects.filter(id=movie_session_id)

        return movie_session
