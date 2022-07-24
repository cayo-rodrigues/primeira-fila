from drf_spectacular.utils import extend_schema


class TicketDetailDocs:
    @extend_schema(summary="Retrieve a ticket")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a ticket")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Update a ticket")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class TicketDocs:
    @extend_schema(summary="List tickets")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Buy tickets")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
