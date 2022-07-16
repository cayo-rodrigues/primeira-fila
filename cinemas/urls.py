from django.urls import path
from movie_sessions import views

from movies.views import MovieByCinemaView
from rooms import views as room_views

from tickets.views import TicketView, TicketUpdateView, TicketSessionMovieDetailsView, TicketSessionMovieOneDetailsView

from .views import CinemaDetailView, CreateCinemaView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
    path("<cine_id>/rooms/", room_views.CreateListRoomView.as_view()),
    path(
        "<cine_id>/rooms/<room_id>/", room_views.UpdateRetrieveDeleteRoomView.as_view()
    ),
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
    path(
        "<cine_id>/movie-sessions/<session_id>/tickets/<ticket_id>/",
        TicketUpdateView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/<session_id>/tickets/",
        TicketSessionMovieDetailsView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/<session_id>/tickets/<ticket_id>/",
        TicketSessionMovieOneDetailsView.as_view(),
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
