from django.urls import path
from .views import CreateCinemaView, CinemaDetailView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
]
