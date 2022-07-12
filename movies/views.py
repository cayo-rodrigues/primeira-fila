from rest_framework import generics
from utils.mixins import SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly

from .models import Movie
from .serializers import ListMoviesSerializer, MovieSerializer


class MovieView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsSuperUser | ReadOnly]
    serializers = {"POST": MovieSerializer, "GET": ListMoviesSerializer}


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperUser | ReadOnly]
    lookup_url_kwarg = "movie_id"


class MovieByCinemaView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        # TODO
        """
        retornar apenas os Movies que estão sendo exibidos em um Cinema,
        isto é, os filmes que tem alguma MovieSession agendada
        """
