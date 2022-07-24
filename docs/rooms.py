from drf_spectacular.utils import extend_schema


class CreateListRoomDocs:
    @extend_schema(summary="List rooms")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a room")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateRetrieveDeleteRoomDocs:
    @extend_schema(summary="Retrieve a room")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a room")
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a room")
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a room")
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
