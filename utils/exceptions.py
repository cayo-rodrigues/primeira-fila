from rest_framework import status
from rest_framework.exceptions import APIException


class CinemaNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Cinema not found"


class RoomNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Room not found"


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
