from cinemas.models import Cinema
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import generics
from utils.mixins import MovieQueryParamsMixin, SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly

from .models import Movie
from .serializers import ListMoviesSerializer, MovieSerializer


class ListAllMoviesView(MovieQueryParamsMixin, generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = ListMoviesSerializer

    def get_queryset(self):
        return self.use_query_params()


class MovieView(
    MovieQueryParamsMixin, SerializerByMethodMixin, generics.ListCreateAPIView
):
    queryset = Movie.objects.filter(
        movie_sessions__session_datetime__gte=now(),
        movie_sessions__on_sale=True,
    ).distinct()
    permission_classes = [IsSuperUser | ReadOnly]
    serializers = {"POST": MovieSerializer, "GET": ListMoviesSerializer}

    def get_queryset(self):
        return self.use_query_params()


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperUser | ReadOnly]
    lookup_url_kwarg = "movie_id"


class MovieByCinemaView(MovieQueryParamsMixin, generics.ListAPIView):
    queryset = Movie.objects.filter(
        movie_sessions__session_datetime__gte=now(),
        movie_sessions__on_sale=True,
    ).distinct()
    serializer_class = ListMoviesSerializer

    def get_queryset(self):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        self.queryset = self.queryset.filter(movie_sessions__room__cinema=cinema)
        return self.use_query_params()
