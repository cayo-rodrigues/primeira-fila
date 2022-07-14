from django.urls import path
from movie_sessions import views
from movies.views import MovieByCinemaView
from rooms.views import CreateRoomView, UpdateRetrieveRoomView
from tickets.views import TicketView

from .views import CinemaDetailView, CreateCinemaView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
    path("<cine_id>/rooms/", CreateRoomView.as_view()),
    path("<cine_id>/rooms/<room_id>/", UpdateRetrieveRoomView.as_view()),
    path(
        "<cine_id>/rooms/<room_id>/movie/<movie_id>/movie-sessions/",
        views.MovieSessionCreateView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/",
        views.MovieSessionCinemaDetailView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/<session_id>/tickets/",
        TicketView.as_view(),
    ),
    path("<cine_id>/movies/", MovieByCinemaView.as_view()),
    path(
        "<cine_id>/movies/<movie_id>/movie-sessions/",
        views.MovieSessionMovieDetailView.as_view(),
    ),
    path(
        "<cine_id>/movies/<movie_id>/movie-sessions/<session_id>/",
        views.MovieSessionDetail.as_view(),
    ),
]
