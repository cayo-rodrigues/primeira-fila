from django.urls import path
from tickets.views import TicketDetailsView

from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("self/", views.UserDetailView.as_view()),
    path("tickets/<ticket_id>/", TicketDetailsView.as_view()),
]
