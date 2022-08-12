from drf_spectacular.utils import extend_schema

USER_REGISTER_DESCRIPTION = (
    "Register a new user. In case you want to register as a cinema manager, you should pass "
    "the key `is_staff` having a value of `true`. Otherwise, you can omit it, since the default "
    "value is `false`."
)

USER_UPDATE_DESCRIPTION = (
    "Update a user's info. Users can only update themselves. No need to pass an id in the url. "
    "**Only authenticated users have access to this route**."
)

USER_RETRIEVE_DESCRIPTION = (
    "Retrieve a user's profile info. Users can only retrieve themselves. No need to pass an id in the url. "
    "**Only authenticated users have access to this route**."
)

USER_DELETE_DESCRIPTION = (
    "Delete a user's account. Users can only delete their own accounts. No need to pass an id in the url. "
    "**Only authenticated users have access to this route**."
)


class UserDetailDocs:
    @extend_schema(
        summary="Retrieve a user's profile", description=USER_RETRIEVE_DESCRIPTION
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update a user's profile", description=USER_UPDATE_DESCRIPTION
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Update a user's profile", description=USER_UPDATE_DESCRIPTION
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a user's profile", description=USER_DELETE_DESCRIPTION
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
