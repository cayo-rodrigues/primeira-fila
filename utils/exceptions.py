from rest_framework import status
from rest_framework.exceptions import APIException


class CinemaNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Cinema not found"


class RoomNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Room not found on this cinema"


class SessionSeatNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Session seat not found or not available"


class SeatNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Seat not found on this room"


class MovieNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Movie not found"


class MovieSessionNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Movie session not found"


class TicketNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Ticket not found"


class ImageNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Image not found"


class AccountConfirmationNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found"


class MovieSessionNotAvailableError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This room is not available for a movie session at this time"


class IdenticalAddressError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "This exact same address is already in use. If your cinema is located inside the same building as another, please set a different 'details' value"


class MovieTitleUnavailableError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Movie with this title already exists"
