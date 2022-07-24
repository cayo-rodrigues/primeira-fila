from drf_spectacular.utils import OpenApiParameter, extend_schema

CINEMA_QUERY_PARAMS = [
    OpenApiParameter("street"),
    OpenApiParameter("district"),
    OpenApiParameter("city"),
    OpenApiParameter("state"),
    OpenApiParameter("country"),
]


class CinemaDocs:
    @extend_schema(parameters=CINEMA_QUERY_PARAMS, summary="List cinemas")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a cinema")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CinemaDetailDocs:
    @extend_schema(summary="Retrieve a cinema")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a cinema")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a cinema")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a cinema")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
