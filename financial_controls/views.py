from rest_framework import generics
from financial_controls.models import UserFinancialControl
from financial_controls.serializers import UserFinancialControlSerializer
from utils.permissions import OwnerPermission

class UserFinancialControlView(generics.RetrieveAPIView):
    permission_classes = [OwnerPermission]
    
    queryset = UserFinancialControl.objects.all()
    serializer_class = UserFinancialControlSerializer
    
    def get_object(self):
        obj = UserFinancialControl.objects.get(user=self.request.user)
        return obj
