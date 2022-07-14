from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from .models import Cinema
from addresses.models import Address
from .serializers import ListCinemaSerializer, CreateCinemaSerializer
from .mixins import SerializeByMethodMixin
from utils.permissions import IsSuperUser, ReadOnly

# import ipdb


class CreateCinemaView(SerializeByMethodMixin, generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly, OnlySellerCreatePermission]

    queryset = Cinema.objects.all()
    serializer_map = {"GET": ListCinemaSerializer, "POST": CreateCinemaSerializer}

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CinemaDetailView(SerializeByMethodMixin, generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [CustomCinemaPermission]

    queryset = Cinema.objects.all()
    serializer_class = CreateCinemaSerializer
    lookup_url_kwarg = "cine_id"
    # permission_classes = [IsSuperUser | ReadOnly]
