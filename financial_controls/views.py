from rest_framework import generics
from financial_controls.models import CinemaFinancialControl, UserFinancialControl
from financial_controls.serializers import CinemaFinancialControlSerializer, UserFinancialControlSerializer
from utils.permissions import OwnerPermission, OnlySelfManagerPermissionFinancial

class UserFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OwnerPermission]
    
    queryset = UserFinancialControl.objects.all()
    serializer_class = UserFinancialControlSerializer
    
    def get_object(self):
        obj = UserFinancialControl.objects.get(user=self.request.user)
        return obj
    
class CinemaFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OnlySelfManagerPermissionFinancial]
    
    queryset = CinemaFinancialControl.objects.all()
    serializer_class = CinemaFinancialControlSerializer 
    lookup_url_kwarg = "cine_id"   
    lookup_field = "cinema_id"
    
    
    def get_object(self):
        obj = CinemaFinancialControl.objects.get(cinema_id=self.kwargs["cine_id"])
        return obj
