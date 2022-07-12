from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name", "age","is_staff", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]
        
    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user    