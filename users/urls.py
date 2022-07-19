from django.urls import path
from financial_controls.views import UserFinancialControlView
from tickets.views import UserTicketDetailsView

from . import views

urlpatterns = [
    path("", views.UserView.as_view()),
    path("self/", views.UserDetailView.as_view()),
    path("tickets/<ticket_id>/", UserTicketDetailsView.as_view()),
    path("accounts/<confirmation_id>/", views.ConfirmAccountView.as_view()),
    path("self/financial-control/", UserFinancialControlView.as_view()),
]
