from django.urls import path
from .views import CreateCinemaView, RetrieveUpdatedCinemaView

urlpatterns = [
    path("", CreateCinemaView.as_view()),
    path("<cine_id>/", RetrieveUpdatedCinemaView.as_view()),
]
