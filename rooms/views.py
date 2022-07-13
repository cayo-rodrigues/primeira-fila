from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from rooms.serializer import (
    RoomSerializer,
)

# Create your views here.


class CreateRoomView(APIView):
    def post(self, request):

        rows_list = request.data["seat_rows"]
        request.data["seat_rows"] = []

        for i, value in enumerate(rows_list):
            letter = chr(65 + i)
            row_dict = {"row": letter, "seat_count": value}
            request.data["seat_rows"].append(row_dict)

        serializer = RoomSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        room = serializer.save()

        serializer.validated_data["id"] = room.id

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
