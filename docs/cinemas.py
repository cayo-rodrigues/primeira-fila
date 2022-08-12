from drf_spectacular.utils import OpenApiParameter, extend_schema

CINEMA_QUERY_PARAMS = [
    OpenApiParameter("street"),
    OpenApiParameter("district"),
    OpenApiParameter("city"),
    OpenApiParameter("state"),
    OpenApiParameter("country"),
]

CINEMA_LIST_DESCRIPTION = (
    "List all registered cinemas. You can use query params to filter the results."
)

CINEMA_REGISTER_DESCRIPTION = (
    "Register a cinema. **To use this route, a user has to be authenticated and be a manager.** "
    "A manager is just an user with the `is_staff` status equal to `True`. A manager may "
    "register as many cinemas as he/she pleases.<br><br>"
    "Cinema addresses are unique. You can't register two cinemas with an identical address. "
    "But in case there are two cinemas in the same building, you could for instance differ "
    "each other's addresses by the `detail` key."
)

CINEMA_UPDATE_DESCRIPTION = (
    "Update a cinema's info. **Only the cinema manager has access to this route.**"
)

CINEMA_DELETE_DESCRIPTION = (
    "Delete a cinema. **Only the cinema manager has access to this route.**"
)

CINEMA_FINANCIAL_DESCRIPTION = (
    "Show total income of all tickets sold by a cinema. "
    "**Only the cinema manager has access to this route.**"
)


class CinemaDocs:
    @extend_schema(
        parameters=CINEMA_QUERY_PARAMS,
        summary="List cinemas",
        description=CINEMA_LIST_DESCRIPTION,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a cinema", description=CINEMA_REGISTER_DESCRIPTION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CinemaDetailDocs:
    @extend_schema(summary="Retrieve a cinema")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a cinema", description=CINEMA_UPDATE_DESCRIPTION)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(summary="Update a cinema", description=CINEMA_UPDATE_DESCRIPTION)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Delete a cinema", description=CINEMA_DELETE_DESCRIPTION)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
