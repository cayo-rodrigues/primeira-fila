from rest_framework import serializers
from tickets.models import Ticket
from users.models import User
from financial_controls.models import UserFinancialControl, CinemaFinancialControl


class UserFinancialControlSerializer(serializers.ModelSerializer):
    expenses = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserFinancialControl
        fields = "__all__"
        
        
    def create(self, validated_data):
        return UserFinancialControl.objects.create(**validated_data)

    
    def get_expenses(self):
        value = 0
        tickets = Ticket.objects.filter(user=self.user)
        for ticket in tickets:
            value += ticket.total
            
        return value    
        
            
      
        
class CinemaFinancialControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaFinancialControl
        fields = "__all__"        