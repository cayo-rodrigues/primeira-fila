from drf_spectacular.utils import extend_schema

SESSION_CREATE_DESCRIPTION = (
    "Schedule a movie session. The movie session date and time can't be less then now, "
    "and two movie sessions in the same room can't take place at the same date and time. "
    "**Only the manager of the cinema can access this route.**"
)

SESSION_UPDATE_DESCRIPTION = (
    "Update a movie session. **Only the manager of the cinema can access this route.**"
)

SESSION_DELETE_DESCRIPTION = (
    "Delete a movie session. **Only the manager of the cinema can access this route.**"
)


class MovieSessionDetailDocs:
    @extend_schema(summary="Retrieve a movie session of a cinema")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a movie session of a cinema",
        description=SESSION_UPDATE_DESCRIPTION,
    )
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a movie session of a cinema",
        description=SESSION_UPDATE_DESCRIPTION,
    )
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a movie session of a cinema",
        description=SESSION_DELETE_DESCRIPTION,
    )
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
