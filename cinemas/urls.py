from django.urls import path
from financial_controls.views import CinemaFinancialControlView
from movie_sessions import views
from movies.views import MovieByCinemaView
from rooms import views as room_views
from tickets.views import TicketDetailView, TicketSessionMovieView, TicketView

from .views import CinemaDetailView, CinemaView

urlpatterns = [
    path("", CinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
    path("<cine_id>/rooms/", room_views.CreateListRoomView.as_view()),
    path(
        "<cine_id>/rooms/<room_id>/", room_views.UpdateRetrieveDeleteRoomView.as_view()
    ),
    path(
        "<cine_id>/rooms/<room_id>/movies/<movie_id>/movie-sessions/",
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
        TicketDetailView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/<session_id>/tickets/",
        TicketSessionMovieView.as_view(),
    ),
    path("<cine_id>/movies/", MovieByCinemaView.as_view()),
    path(
        "<cine_id>/movies/<movie_id>/movie-sessions/",
        views.MovieSessionMovieDetailView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/<session_id>/",
        views.MovieSessionDetail.as_view(),
    ),
    path("<cine_id>/financial-control/", CinemaFinancialControlView.as_view()),
]
