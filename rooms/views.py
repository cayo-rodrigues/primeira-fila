from cinemas.models import Cinema
from django.shortcuts import get_object_or_404
from rest_framework import generics
from utils.exceptions import CinemaNotFoundError
from utils.helpers import safe_get_list_or_404, safe_get_object_or_404

from rooms.models import Room
from rooms.serializers import RoomSerializer

# Create your views here.


class CreateListRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return safe_get_list_or_404(
            self.queryset, CinemaNotFoundError, cinema_id=self.kwargs["cine_id"]
        )
        # return self.queryset.filter(cinema_id=self.kwargs["cine_id"])

    def perform_create(self, serializer):
        cinema = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, pk=self.kwargs["cine_id"]
        )
        # cinema = get_object_or_404(pk=self.kwargs['cine_id'])
        serializer.save(cinema=cinema)


class UpdateRetrieveDeleteRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, pk=self.kwargs["room_id"], cinema_id=self.kwargs["cine_id"]
        )

        return obj
