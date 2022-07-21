from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.permissions import OnlySelfManagerPermissionFinancial, OwnerPermission

from financial_controls.models import CinemaFinancialControl, UserFinancialControl
from financial_controls.serializers import (
    CinemaFinancialControlSerializer,
    UserFinancialControlSerializer,
)


from drf_spectacular.utils import extend_schema



class UserFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OwnerPermission]

    queryset = UserFinancialControl.objects.all()
    serializer_class = UserFinancialControlSerializer

    def get_object(self):
        obj = UserFinancialControl.objects.get(user=self.request.user)
        return obj

@extend_schema(
    operation_id="list_finances",
    tags=["list finances of a cinema"]
)
class CinemaFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OnlySelfManagerPermissionFinancial, IsAuthenticated]

    queryset = CinemaFinancialControl.objects.all()
    serializer_class = CinemaFinancialControlSerializer
    lookup_url_kwarg = "cine_id"
    lookup_field = "cinema_id"
