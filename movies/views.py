from faulthandler import disable

from rest_framework import generics
from utils.helpers import normalize_text
from utils.mixins import SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly

from .models import Movie
from .serializers import ListMoviesSerializer, MovieSerializer


class MovieView(SerializerByMethodMixin, generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsSuperUser | ReadOnly]
    serializers = {"POST": MovieSerializer, "GET": MovieSerializer}

    def get_queryset(self):
        age_group = self.request.GET.get("age_group")
        age_group_lt = self.request.GET.get("age_group_lt")
        age_group_gt = self.request.GET.get("age_group_gt")
        distributor = self.request.GET.get("distributor")
        genres = self.request.GET.get("genres")

        if age_group:
            self.queryset = self.queryset.filter(age_group__minimum_age=age_group)
        else:
            if age_group_lt:
                self.queryset = self.queryset.filter(
                    age_group__minimum_age__lt=age_group_lt
                )
            if age_group_gt:
                self.queryset = self.queryset.filter(
                    age_group__minimum_age__gt=age_group_gt
                )

        if distributor:
            self.queryset = self.queryset.filter(
                distributor__name__icontains=distributor.strip()
            )
        if genres:
            self.queryset = self.queryset.filter(genres__name__in=genres.split(","))

        return self.queryset


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
