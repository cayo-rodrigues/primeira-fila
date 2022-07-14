from django.urls import path

from . import views

urlpatterns = [
    path("", views.MovieView.as_view()),
    path("all/", views.ListAllMoviesView.as_view()),
    path("<movie_id>/", views.MovieDetailView.as_view()),
]
