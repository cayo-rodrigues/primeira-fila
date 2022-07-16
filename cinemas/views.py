from rest_framework import generics
from utils.permissions import OnlySelfManagerPermission

from .mixins import SerializeByMethodMixin
from .models import Cinema
from .serializers import CreateCinemaSerializer, ListCinemaSerializer


class CreateCinemaView(SerializeByMethodMixin, generics.ListCreateAPIView):

    queryset = Cinema.objects.all()
    serializer_map = {"GET": ListCinemaSerializer, "POST": CreateCinemaSerializer}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CinemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CreateCinemaSerializer
    lookup_url_kwarg = "cine_id"
    permission_classes = [OnlySelfManagerPermission]
