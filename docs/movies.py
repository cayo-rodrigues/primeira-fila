from drf_spectacular.utils import OpenApiParameter, extend_schema

MOVIE_QUERY_PARAMS = [
    OpenApiParameter("age_group", int),
    OpenApiParameter("age_group_lte", int, description="Less than or equal to"),
    OpenApiParameter("age_group_gte", int, description="Greater than or equal to"),
    OpenApiParameter("distributor"),
    OpenApiParameter("genres", description="Comma separated values of lowercase genres"),
]

MOVIE_LIST_ALL_DESCRIPTION = "List all registered movies, including those having no movie sessions related to them."

MOVIE_LIST_DESCRIPTION = (
    "List all playing movies, that is, all movies having at least one movie session related to them, "
    "scheduled for now or anytime in the future."
)

MOVIE_REGISTER_DESCRIPTION = (
    "Register a new movie. **Only the system admins can access this route**."
)

MOVIE_UPDATE_DESCRIPTION = (
    "Update a movie's info. **Only the system admins can access this route**."
)

MOVIE_DELETE_DESCRIPTION = (
    "Delete a movie. **Only the system admins can access this route**."
)

MOVIE_IMG_UPLOAD_DESCRIPTION = (
    "Upload an image for a movie. **Only the system admins can access this route**. "
    "A movie may have more than one image, but each image must be uploaded once at a time.<br><br>"
    "This route has a throttling of 3/day, therefore, only 3 images can be uploaded each 24 hours. "
    "**The max upload size is 2MB.**"
)

MOVIE_IMG_UPDATE_DESCRIPTION = (
    "Update a movie's image. **Only the system admins can access this route**. "
    "This route is protected by the same throttling system of the `POST` route, "
    "so both routes decrease the count of available requests."
)

MOVIE_IMG_DELETE_DESCRIPTION = (
    "Delete a movie's image. **Only the system admins can access this route**."
)


class MovieDocs:
    @extend_schema(
        parameters=MOVIE_QUERY_PARAMS,
        summary="List playing movies",
        description=MOVIE_LIST_DESCRIPTION,
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Register a movie", description=MOVIE_REGISTER_DESCRIPTION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class MovieDetailDocs:
    @extend_schema(summary="Retrieve a movie")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a movie", description=MOVIE_UPDATE_DESCRIPTION)
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Retrieve a movie", description=MOVIE_UPDATE_DESCRIPTION)
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Delete a movie", description=MOVIE_DELETE_DESCRIPTION)
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MovieImageDetailDocs:
    @extend_schema(summary="Retrieve an image of a movie")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update an image of a movie", description=MOVIE_IMG_UPDATE_DESCRIPTION
    )
    def put(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update an image of a movie", description=MOVIE_IMG_UPDATE_DESCRIPTION
    )
    def patch(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an image of a movie", description=MOVIE_IMG_DELETE_DESCRIPTION
    )
    def delete(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
