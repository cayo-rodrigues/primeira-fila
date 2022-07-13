from django.urls import path


from . import views

urlpatterns = [
    path(
        "str:<cine_id>/room/str:<room_id>/movie/str:<movie_id>/movie-sessions/",
        views.MovieSessionCreateView.as_view(),
    ),
    path(
        "str:<cine_id>/movie-sessions/",
        views.MovieSessionCinemaDetailView.as_view(),
    ),
    path(
        "str:<cine_id>/movies/str:<movie_id>/movie-sessions/",
        views.MovieSessionMovieDetailView.as_view(),
    ),
    path(
        "str:<cine_id>/movies/str:<movie_id>/movie-sessions/str:<session_id>/",
        views.MovieSessionDetail.as_view(),
    ),
]
