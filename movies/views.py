from rest_framework import generics
from utils.mixins import SerializerByMethodMixin
from utils.permissions import IsSuperUser

from .models import Movie
from .serializers import ListMoviesSerializer, MovieSerializer


class MovieView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsSuperUser]
    serializers = {"POST": MovieSerializer, "GET": ListMoviesSerializer}


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperUser]
    lookup_url_kwarg = "movie_id"
