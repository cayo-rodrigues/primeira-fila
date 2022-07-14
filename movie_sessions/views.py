from cinemas.models import Cinema
from django.shortcuts import get_object_or_404, render
from movies.models import Movie
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rooms.models import Room

from .models import MovieSession
from .serializers import MovieSessionSerializer


class MovieSessionCreateView(generics.CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def perform_create(self, serializer):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        room = get_object_or_404(Room, pk=self.kwargs["room_id"], cinema=cinema)
        movie = get_object_or_404(Movie, pk=self.kwargs["movie_id"])

        serializer.save(cinema=cinema, room=room, movie=movie)


class MovieSessionCinemaDetailView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]

        cinema = get_object_or_404(Cinema, id=cinema_id)

        movie_sessions = MovieSession.objects.filter(cinema_id=cinema_id)

        return movie_sessions


class MovieSessionMovieDetailView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def get_queryset(self):

        cinema_id = self.kwargs["cine_id"]
        movie_id = self.kwargs["movie_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(Movie, id=movie_id)

        movie_sessions = MovieSession.objects.filter(movie_id=movie_id)

        return movie_sessions


class MovieSessionDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer

    def get_queryset(self):
        cinema_id = self.kwargs["cine_id"]
        movie_id = self.kwargs["movie_id"]
        movie_session_id = self.kwargs["session_id"]

        get_object_or_404(Cinema, id=cinema_id)
        get_object_or_404(Movie, id=movie_id)
        get_object_or_404(MovieSession, id=movie_session_id)

        movie_session = MovieSession.objects.filter(movie_id=movie_id)

        return movie_session
