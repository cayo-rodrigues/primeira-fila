from drf_spectacular.utils import extend_schema


class MovieSessionDetailDocs:
    @extend_schema(summary="Retrieve a movie session of a cinema")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a movie session of a cinema")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a movie session of a cinema")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a movie session of a cinema")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
