from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
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
        user = User.objects.create(**validated_data)
        UserFinancialControl.objects.create(user=user)
        confirmation = AccountConfirmation.objects.create(account=user)

        current_host = self.context["request"].get_host()

        # send_mail(
        #    subject="Confirmação de conta no site Primeira Fila",
        #    message="",
        #    html_message=f"<h2>Olá, {user.first_name}! Muito obrigado por usar o Primeira Fila.</h2>"
        #    "<p>Clique no seguinte link para ativar sua conta:</p>"
        #    f"<p>{current_host}/users/accounts/{confirmation.id}/</p>"
        #    "<p>Atenciosamente, equipe Primeira Fila :)</p>",
        #    from_email=EMAIL_HOST_USER,
        #    recipient_list=[user.email],
        #    fail_silently=False,
        # )
        user.is_active = True
        user.save()

        return user
