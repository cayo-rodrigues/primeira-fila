from django.urls import path
from . import views

urlpatterns = [
    path("cinemas/rooms/", views.CreateRoomView.as_view()),
    # path("cinemas/rooms/<int:pk>", views.UpddateRoomView.as_view()),
]
