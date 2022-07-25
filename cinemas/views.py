from docs.cinemas import CinemaDetailDocs, CinemaDocs
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from utils.mixins import SerializerByMethodMixin
from utils.permissions import OnlySelfManagerPermission

from .models import Cinema
from .serializers import CreateCinemaSerializer, ListCinemaSerializer


@extend_schema(
    operation_id="create_list_cinema",
    tags=["cinemas"],
)
class CinemaView(CinemaDocs, SerializerByMethodMixin, generics.ListCreateAPIView):

    queryset = Cinema.objects.all()
    serializers = {"GET": ListCinemaSerializer, "POST": CreateCinemaSerializer}

    def get_queryset(self):
        street = self.request.GET.get("street")
        district = self.request.GET.get("district")
        city = self.request.GET.get("city")
        state = self.request.GET.get("state")
        country = self.request.GET.get("country")

        if street:
            self.queryset = Cinema.objects.filter(address__street__icontains=street)

        if district:
            self.queryset = self.queryset.filter(
                address__district__name__icontains=district
            )

        if city:
            self.queryset = self.queryset.filter(address__city__name__icontains=city)

        if state:
            self.queryset = self.queryset.filter(address__state__name__icontains=state)

        if country:
            self.queryset = self.queryset.filter(
                address__country__name__icontains=country
            )

        return self.queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(
    operation_id="retrieve_update_delete_cinema",
    tags=["cinemas"],
)
class CinemaDetailView(CinemaDetailDocs, generics.RetrieveUpdateDestroyAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CreateCinemaSerializer
    lookup_url_kwarg = "cine_id"
    permission_classes = [OnlySelfManagerPermission]
