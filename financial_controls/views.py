from rest_framework import generics
from financial_controls.models import CinemaFinancialControl, UserFinancialControl
from financial_controls.serializers import CinemaFinancialControlSerializer, UserFinancialControlSerializer
from utils.permissions import OwnerPermission, OnlySelfManagerPermissionFinancial
from rest_framework.permissions import IsAuthenticated


class UserFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OwnerPermission]
    
    queryset = UserFinancialControl.objects.all()
    serializer_class = UserFinancialControlSerializer
    
    def get_object(self):
        obj = UserFinancialControl.objects.get(user=self.request.user)
        return obj
    
class CinemaFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OnlySelfManagerPermissionFinancial, IsAuthenticated]
    
    queryset = CinemaFinancialControl.objects.all()
    serializer_class = CinemaFinancialControlSerializer 
    lookup_url_kwarg = "cine_id"   
    lookup_field = "cinema_id"
