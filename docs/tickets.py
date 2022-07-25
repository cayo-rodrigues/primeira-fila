from drf_spectacular.utils import extend_schema

TICKET_BUY_DESCRIPTION = (
    "Buy a ticket. To buy a ticket for a movie, you only gotta choose your seats. "
    "**Only authenticated users can access this route**. Upon buying a ticket, a confirmation "
    "is sent by email, specifying details about the user, the movie session and the cinema related "
    "to the ticket. Also, a link to a QRCode is sent. This QRCode is meant to be presented at the "
    "cinema, so that a user can prove that he/she has got a valid ticket."
)

TICKET_RETRIEVE_DESCRIPTION = (
    "Retrieve a ticket. The url for this route is encoded in the QRCode sent upon buying a ticket. "
    "It can be used to prove that a ticket is valid."
)

TICKET_UPDATE_DESCRIPTION = (
    "Update a ticket's chosen seats. **Only authenticated users can access this route**. Users can "
    "change their seats, but they cannot change how many seats they bought."
)


class TicketDocs:
    @extend_schema(summary="List tickets")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Buy tickets", description=TICKET_BUY_DESCRIPTION)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TicketDetailDocs:
    @extend_schema(summary="Retrieve a ticket", description=TICKET_RETRIEVE_DESCRIPTION)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Update a ticket", description=TICKET_UPDATE_DESCRIPTION)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(summary="Update a ticket", description=TICKET_UPDATE_DESCRIPTION)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
