
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
from rooms.serializer import RoomSerializer

# Create your views here.


class CreateRoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(cinema_id=kwargs["cine_id"])
        try:
            Cinema.objects.get(pk=kwargs["cine_id"])
        except:
            raise Http404()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        cinema = get_object_or_404(Cinema, pk=self.kwargs["cine_id"])
        serializer.save(cinema=cinema)



class UpdateRetrieveRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(
            cinema_id=kwargs["cine_id"], id=kwargs["room_id"]
        )
        try:
            Cinema.objects.get(pk=kwargs["cine_id"])
        except:
            raise Http404()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data[0])

    def destroy(self, request, *args, **kwargs):

        try:
            single_room = self.get_queryset().filter(
                cinema_id=kwargs["cine_id"], id=kwargs["room_id"]
            )[0]
            Cinema.objects.get(pk=kwargs["cine_id"])
        except:
            raise Http404()

        self.perform_destroy(single_room)

        return Response(status=status.HTTP_204_NO_CONTENT)
