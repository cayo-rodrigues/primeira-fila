from django.urls import path
from rooms.views import CreateRoomView

from .views import CinemaDetailView, CreateCinemaView

from movie_sessions import views

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
    path("<cine_id>/rooms/", CreateRoomView.as_view()),
    path(
        "<cine_id>/room/<room_id>/movie/<movie_id>/movie-sessions/",
        views.MovieSessionCreateView.as_view(),
    ),
    path(
        "<cine_id>/movie-sessions/",
        views.MovieSessionCinemaDetailView.as_view(),
    ),
    path(
        "<cine_id>/movies/<movie_id>/movie-sessions/",
        views.MovieSessionMovieDetailView.as_view(),
    ),
    path(
        "<cine_id>/movies/<movie_id>/movie-sessions/<session_id>/",
        views.MovieSessionDetail.as_view(),
    ),
]