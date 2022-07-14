from django.urls import path

from . import views

urlpatterns = [
    path("cinemas/<cine_id>/movie_sessions/<movie_sessions_id>/tickets/", views.TicketView.as_view()),
    path("user/tickets/<ticket_id>/", views.TicketDetailsView.as_view()),
]