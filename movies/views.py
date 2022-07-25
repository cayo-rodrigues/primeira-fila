from cinemas.models import Cinema
from django.utils.timezone import now
from docs.movies import (
    MOVIE_IMG_UPLOAD_DESCRIPTION,
    MOVIE_LIST_ALL_DESCRIPTION,
    MOVIE_QUERY_PARAMS,
    MovieDetailDocs,
    MovieDocs,
    MovieImageDetailDocs,
)
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from utils.exceptions import CinemaNotFoundError, ImageNotFoundError, MovieNotFoundError
from utils.helpers import safe_get_object_or_404
from utils.mixins import MovieQueryParamsMixin, SerializerByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly
from utils.throttles import MovieImgUploadRateThrottle

from .models import Image, Movie
from .serializers import ImageSerializer, ListMoviesSerializer, MovieSerializer


@extend_schema(
    operation_id="list_movies",
    tags=["movies"],
    summary="List all movies",
    parameters=MOVIE_QUERY_PARAMS,
    description=MOVIE_LIST_ALL_DESCRIPTION,
)
class ListAllMoviesView(MovieQueryParamsMixin, generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = ListMoviesSerializer

    def get_queryset(self):
        return self.use_query_params()


@extend_schema(
    operation_id="list_create_movies",
    tags=["movies"],
)
class MovieView(
    MovieDocs, MovieQueryParamsMixin, SerializerByMethodMixin, generics.ListCreateAPIView
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
    tags=["movies"],
)
class MovieDetailView(MovieDetailDocs, generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsSuperUser | ReadOnly]
    lookup_url_kwarg = "movie_id"


@extend_schema(
    operation_id="list_movies",
    tags=["movies"],
    parameters=MOVIE_QUERY_PARAMS,
    summary="List playing movies by cinema",
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
    tags=["movies"],
    summary="Upload an image for a movie",
    description=MOVIE_IMG_UPLOAD_DESCRIPTION,
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
    tags=["movies"],
)
class MovieImageDetailView(MovieImageDetailDocs, generics.RetrieveUpdateDestroyAPIView):
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
