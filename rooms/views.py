from django.http import Http404
from django.shortcuts import render
from jsonschema import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from cinemas.models import Cinema
from rooms.models import Room

from cinemas.models import Cinema
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView


from rooms.models import Room
from rooms.serializers import RoomSerializer

# Create your views here.


class CreateListRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        cinema = self.queryset.filter(cinema_id=self.kwargs["cine_id"])

        return cinema


class UpdateRetrieveDeleteRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, pk=self.kwargs["room_id"], cinema_id=self.kwargs["cine_id"]
        )

        return obj
