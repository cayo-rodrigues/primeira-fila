from django.urls import path
from .views import CreateCinemaView, CinemaDetailView
from rooms.views import CreateRoomView, UpdateRetrieveRoomView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<int:cine_id>/", CinemaDetailView.as_view()),
    path("<int:cine_id>/rooms/", CreateRoomView.as_view()),
    path("<int:cine_id>/rooms/<str:room_id>/", UpdateRetrieveRoomView.as_view()),
]
