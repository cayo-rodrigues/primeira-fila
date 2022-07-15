from cinemas.models import Cinema
from django.shortcuts import get_object_or_404
from rest_framework import generics

from rooms.models import Room
from rooms.serializers import RoomSerializer, UpdateRoomSerializer
from utils.mixins import SerializerByMethodMixin

# Create your views here.


class CreateListRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        cinema = self.queryset.filter(cinema_id=self.kwargs["cine_id"])

        return cinema

    def perform_create(self, serializer):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        serializer.save(cinema=cinema)


class UpdateRetrieveDeleteRoomView(
    SerializerByMethodMixin, generics.RetrieveUpdateDestroyAPIView
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    serializers = {
        "PATCH": UpdateRoomSerializer,
        "GET": RoomSerializer,
        "DELETE": RoomSerializer,
    }

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, pk=self.kwargs["room_id"], cinema_id=self.kwargs["cine_id"]
        )

        return obj
