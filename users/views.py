from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from users.models import AccountConfirmation, User
from users.serializers import UserSerializer


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = User.objects.get(email=self.request.user)
        return obj


class ConfirmAccountView(generics.RetrieveAPIView):
    queryset = AccountConfirmation.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        confirmation = get_object_or_404(
            AccountConfirmation, pk=self.kwargs["confirmation_id"]
        )
        confirmation.account.is_active = True
        confirmation.account.save()
        return Response(
            {"name": confirmation.account.first_name},
            template_name="users/account_confirmation.html",
        )
