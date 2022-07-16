from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import AccountConfirmation, User
from users.serializers import UserSerializer


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = User.objects.get(email=self.request.user)
        return obj


class ConfirmAccountView(generics.RetrieveAPIView):
    queryset = AccountConfirmation.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        confirmation = get_object_or_404(
            AccountConfirmation, pk=self.kwargs["confirmation_id"]
        )
        confirmation.account.is_active = True
        confirmation.account.save()
        return confirmation.account
