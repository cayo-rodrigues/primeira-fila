from cinemas.models import Cinema
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from utils.exceptions import CinemaNotFoundError, RoomNotFoundError
from utils.helpers import safe_get_list_or_404, safe_get_object_or_404
from utils.permissions import OnlySelfManagerPermission, ReadOnly

from rooms.models import Room
from rooms.serializers import RoomSerializer

# Create your views here.


@extend_schema(
    operation_id="room_get_post",
    request=RoomSerializer,
    responses=RoomSerializer,
    tags=["Create / List Rooms of a Cinema"],
)
class CreateListRoomView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        return safe_get_list_or_404(
            self.queryset, CinemaNotFoundError, cinema_id=self.kwargs["cine_id"]
        )

    def perform_create(self, serializer):
        cinema = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, pk=self.kwargs["cine_id"]
        )

        if self.request.user.id != cinema.owner.id:
            raise PermissionDenied()

        serializer.save(cinema=cinema)


@extend_schema(
    operation_id="room_get_update_delete",
    request=RoomSerializer,
    responses=RoomSerializer,
    tags=["Retrieve / Update / Delete a Room"],
)
class UpdateRetrieveDeleteRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [OnlySelfManagerPermission]

    def get_object(self):
        obj = safe_get_object_or_404(
            Room,
            RoomNotFoundError,
            pk=self.kwargs["room_id"],
            cinema_id=self.kwargs["cine_id"],
        )
        cinema = safe_get_object_or_404(
            Cinema, CinemaNotFoundError, pk=self.kwargs["cine_id"]
        )

        self.check_object_permissions(self.request, cinema)

        return obj
