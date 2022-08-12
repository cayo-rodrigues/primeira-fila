from drf_spectacular.utils import extend_schema

ROOM_LIST_DESCRIPTION = "List all rooms of a cinema."

ROOM_REGISTER_DESCRIPTION = (
    "Register a new room for a cinema. **Only the manager of the cinema can access this route.** "
    "The idea of this route is to allow a manager to precisely describe the structure of the room, "
    "specifying each row of seats and the room corridors."
)

ROOM_UPDATE_DESCRIPTION = "Update a room's structural info. **Only the manager of the cinema can access this route.**"

ROOM_DELETE_DESCRIPTION = "Delete a room from a cinema. **Only the manager of the cinema can access this route.**"


class CreateListRoomDocs:
    @extend_schema(summary="List rooms", description=ROOM_LIST_DESCRIPTION)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a room", description=ROOM_REGISTER_DESCRIPTION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UpdateRetrieveDeleteRoomDocs:
    @extend_schema(summary="Retrieve a room")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a room", description=ROOM_UPDATE_DESCRIPTION)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Update a room", description=ROOM_UPDATE_DESCRIPTION)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Delete a room", description=ROOM_DELETE_DESCRIPTION)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
