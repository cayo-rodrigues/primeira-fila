from docs.users import USER_REGISTER_DESCRIPTION, UserDetailDocs
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from utils.exceptions import AccountConfirmationNotFoundError
from utils.helpers import safe_get_object_or_404

from users.models import AccountConfirmation, User
from users.serializers import UserSerializer


@extend_schema(summary="Register a user", description=USER_REGISTER_DESCRIPTION)
class UserView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(UserDetailDocs, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        obj = User.objects.get(email=self.request.user)
        return obj


@extend_schema(
    summary="Confirm a user's account",
    description="The url for this route is sent through email upon registration",
    tags=["users"],
)
class ConfirmAccountView(generics.RetrieveAPIView):
    queryset = AccountConfirmation.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        confirmation = safe_get_object_or_404(
            AccountConfirmation,
            AccountConfirmationNotFoundError,
            pk=self.kwargs["confirmation_id"],
        )
        confirmation.account.is_active = True
        confirmation.account.save()
        return Response(
            {"name": confirmation.account.first_name},
            template_name="users/account_confirmation.html",
        )
