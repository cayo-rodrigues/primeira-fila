from cinemas.models import Cinema
from django.utils.timezone import now
from rest_framework import generics
from utils.exceptions import CinemaNotFoundError, ImageNotFoundError, MovieNotFoundError
from utils.helpers import safe_get_object_or_404
from utils.mixins import MovieQueryParamsMixin, SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly
from utils.throttles import MovieImgUploadRateThrottle

from .models import Image, Movie
from .serializers import ImageSerializer, ListMoviesSerializer, MovieSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(
    operation_id="list_movies",
    tags=['list all movies']
)
class ListAllMoviesView(MovieQueryParamsMixin, generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = ListMoviesSerializer

    def get_queryset(self):
        return self.use_query_params()

@extend_schema(
    operation_id="list_create_movies",
    tags=['create/list movies in sessions']
)
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

@extend_schema(
    operation_id="retrieve_update_delete_movie",
    tags=['retrieve/update/delete a movie']
)
class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperUser | ReadOnly]
    lookup_url_kwarg = "movie_id"

@extend_schema(
    operation_id="list_movies",
    tags=['list movies in session by cinema']
)
class MovieByCinemaView(MovieQueryParamsMixin, generics.ListAPIView):
    queryset = Movie.objects.filter(
        movie_sessions__session_datetime__gte=now(),
        movie_sessions__on_sale=True,
    ).distinct()
    serializer_class = ListMoviesSerializer

    def get_queryset(self):
        cinema = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, pk=self.kwargs["cine_id"]
        )
        self.queryset = self.queryset.filter(movie_sessions__room__cinema=cinema)
        return self.use_query_params()

@extend_schema(
    operation_id="create_image_movie",
    tags=['upload a image of a movie']
)
class MovieImageUploadView(generics.CreateAPIView):
    queryset = Image.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = ImageSerializer
    throttle_classes = [MovieImgUploadRateThrottle]

    def perform_create(self, serializer):
        movie = safe_get_object_or_404(
            Movie, MovieNotFoundError, pk=self.kwargs["movie_id"]
        )
        serializer.save(movie=movie)

@extend_schema(
    operation_id="retrieve_update_delete_image_movie",
    tags=['retrieve/update/delete a image of a movie']
)
class MovieImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = ImageSerializer
    throttles = {
        "PATCH": [MovieImgUploadRateThrottle],
        "PUT": [MovieImgUploadRateThrottle],
    }

    def get_throttles(self):
        self.throttle_classes = self.throttles.get(self.request.method, [])
        return super().get_throttles()

    def get_object(self):
        movie = safe_get_object_or_404(
            Movie, MovieNotFoundError, pk=self.kwargs["movie_id"]
        )
        return safe_get_object_or_404(
            Image, ImageNotFoundError, movie=movie, pk=self.kwargs["image_id"]
        )
