from financial_controls.models import UserFinancialControl
from rest_framework import serializers

from users.models import AccountConfirmation, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "age",
            "is_staff",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user: User = User.objects.create(**validated_data)
        UserFinancialControl.objects.create(user=user)
        AccountConfirmation.objects.create(account=user)

        user.send_confirmation_email(self.context["request"])
        user.is_active = True
        user.save()

        return user
