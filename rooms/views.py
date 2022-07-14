from cinemas.models import Cinema
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.models import Room
from rooms.serializer import RoomSerializer

# Create your views here.


class CreateRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def perform_create(self, serializer):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        serializer.save(cinema=cinema)


class UpddateRoomView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
