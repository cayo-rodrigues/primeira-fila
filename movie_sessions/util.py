from utils.exceptions import MovieSessionNotAvailableError

from .models import MovieSession


def validate_session_datetime(session_datetime, room, session=None, **kwargs):
    movie_session = MovieSession.objects.filter(
        session_datetime=session_datetime,
        room=room,
        **kwargs,
    )

    if session:
        movie_session = movie_session.exclude(pk=session.id)

    if movie_session.exists():
        raise MovieSessionNotAvailableError
