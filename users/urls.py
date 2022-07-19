from django.urls import path
from financial_controls.views import UserFinancialControlView
from tickets.views import TicketDetailsView

from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("self/", views.UserDetailView.as_view()),
    path("tickets/<ticket_id>/", TicketDetailsView.as_view()),
    path("accounts/<confirmation_id>/", views.ConfirmAccountView.as_view()),
    path("self/financial_control/", UserFinancialControlView.as_view())
]
