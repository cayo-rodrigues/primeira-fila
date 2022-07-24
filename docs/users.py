from drf_spectacular.utils import extend_schema


class UserDetailDocs:
    @extend_schema(summary="Retrieve a user's profile")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a user's profile")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a user's profile")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a user's profile")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
