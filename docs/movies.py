from drf_spectacular.utils import OpenApiParameter, extend_schema

MOVIE_QUERY_PARAMS = [
    OpenApiParameter("age_group", int),
    OpenApiParameter("age_group_lte", int, description="Less than or equal to"),
    OpenApiParameter("age_group_gte", int, description="Greater than or equal to"),
    OpenApiParameter("distributor"),
    OpenApiParameter("genres", description="Comma separated values of lowercase genres"),
]


class MovieDocs:
    @extend_schema(parameters=MOVIE_QUERY_PARAMS, summary="List playing movies")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a movie")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MovieDetailDocs:
    @extend_schema(summary="Retrieve a movie")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a movie")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Retrieve a movie")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a movie")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MovieImageDetailDocs:
    @extend_schema(summary="Retrieve an image of a movie")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update an image of a movie")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update an image of a movie")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete an image of a movie")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
