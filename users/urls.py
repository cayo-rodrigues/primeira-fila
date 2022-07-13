from django.urls import path

from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("self/", views.UserDetailView.as_view()),
]
