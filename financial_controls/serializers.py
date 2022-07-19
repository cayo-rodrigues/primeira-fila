from rest_framework import serializers
from tickets.models import Ticket
from movie_sessions.models import SessionSeat
from financial_controls.models import UserFinancialControl, CinemaFinancialControl


class UserFinancialControlSerializer(serializers.ModelSerializer):
    expenses = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserFinancialControl
        fields = "__all__"
        
        
    def create(self, validated_data):
        return UserFinancialControl.objects.create(**validated_data)

    
    def get_expenses(self, financial_control:UserFinancialControl):
        user = financial_control.user
        tickets = Ticket.objects.filter(user=user)
        value = 0      
        for ticket in tickets:
            actual_movie_session_price = ticket.movie_session.price
            user_session_seats = SessionSeat.objects.filter(ticket_id=ticket.id)
            value += len(user_session_seats)*actual_movie_session_price
            
        return value    
        
            
      
        
class CinemaFinancialControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaFinancialControl
        fields = "__all__"        