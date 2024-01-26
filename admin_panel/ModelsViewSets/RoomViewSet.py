
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from admin_panel.models import Room
from admin_panel.serializers import RoomSerializer


class RoomViewSet(viewsets.ViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, floor_pk=None):
        rooms = Room.objects.filter(floor__id=floor_pk)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def create(self, request, floor_pk=None):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(floor_id=floor_pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, floor_pk=None):
        room = Room.objects.get(pk=pk, floor__id=floor_pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            floor_pk = request.query_params.get('floor_pk')
            if not floor_pk:
                return Response({"error": "Floor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            room = get_object_or_404(Room, pk=pk, floor__id=floor_pk)
            print(room)
            serializer = RoomSerializer(instance=room, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None, floor_pk=None):
        room = Room.objects.get(pk=pk, floor__id=floor_pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
