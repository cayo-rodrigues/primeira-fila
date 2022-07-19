from rest_framework import generics
from utils.mixins import SerializerByMethodMixin
from utils.permissions import OnlySelfManagerPermission

from .models import Cinema
from .serializers import CreateCinemaSerializer, ListCinemaSerializer


class CreateCinemaView(SerializerByMethodMixin, generics.ListCreateAPIView):

    queryset = Cinema.objects.all()
    serializers = {"GET": ListCinemaSerializer, "POST": CreateCinemaSerializer}

    def get_queryset(self):
        street = self.request.GET.get("street")
        district = self.request.GET.get("district")
        city = self.request.GET.get("city")
        state = self.request.GET.get("state")
        country = self.request.GET.get("country")

        if street:
            self.queryset = Cinema.objects.filter(address__street__iexact=street)

        if district:
            self.queryset = self.queryset.filter(
                address__district__name__iexact=district
            )

        if city:
            self.queryset = self.queryset.filter(address__city__name__iexact=city)

        if state:
            self.queryset = self.queryset.filter(address__state__name__iexact=state)

        if country:
            self.queryset = self.queryset.filter(address__country__name__iexact=country)

        return self.queryset
        # return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CinemaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CreateCinemaSerializer
    lookup_url_kwarg = "cine_id"
    permission_classes = [OnlySelfManagerPermission]
