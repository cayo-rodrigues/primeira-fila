from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from users.models import AccountConfirmation, User
from users.serializers import UserSerializer

from drf_spectacular.utils import extend_schema


@extend_schema(
    operation_id="users_post",
    request=UserSerializer,
    responses=UserSerializer,
    description = 'Route for creation of users', 
    summary='Criation of users',
)
class UserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    operation_id="users_retrieve_patch_delete",
    request=UserSerializer,
    responses=UserSerializer,
    description = 'Retrive a user for list, update or delete', 
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = User.objects.get(email=self.request.user)
        return obj

@extend_schema(
    operation_id="users_get",
    request=UserSerializer,
    responses=UserSerializer,
    description = 'Route for confirm creation of a account', 
    summary='Confirmarion of a account',
)
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
