from django.urls import path
from rooms.views import CreateRoomView

from .views import CinemaDetailView, CreateCinemaView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", CinemaDetailView.as_view()),
    path("<cine_id>/rooms/", CreateRoomView.as_view()),
]
