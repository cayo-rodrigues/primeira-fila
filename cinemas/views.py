from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .models import Cinema
from addresses.models import Address
from .serializers import ListCinemaSerializer, CreateCinemaSerializer
from .mixins import SerializeByMethodMixin
from .permissions import CustomCinemaPermission, OnlySellerCreatePermission
import ipdb


class CreateCinemaView(SerializeByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly, OnlySellerCreatePermission]

    queryset = Cinema.objects.all()
    serializer_map = {"GET": ListCinemaSerializer, "POST": CreateCinemaSerializer}

    # def perform_create(self, serializer):
    #     ipdb.set_trace()
    #     objAddress = Address.objects.create(**self.request.data.address)
    #     return serializer.save(owner=self.request.user, address=objAddress)

    def create(self, request, *args, **kwargs):

        address = request.data.pop("address")
        objAddress = Address.objects.create(**address)
        serializer = self.get_serializer(data=request.data)
        print("teste1")
        serializer.is_valid(raise_exception=True)
        print("teste2")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class RetrieveUpdatedCinemaView(SerializeByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [CustomCinemaPermission]

    queryset = Cinema.objects.all()
    serializer_map = {"GET": ListCinemaSerializer, "PATCH": CreateCinemaSerializer}


# Create your views here.
