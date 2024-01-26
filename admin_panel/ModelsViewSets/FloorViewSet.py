from rest_framework import viewsets, status
from rest_framework.response import Response

from admin_panel.models import Floor
from admin_panel.serializers import FloorSerializer


class FloorViewSet(viewsets.ViewSet):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer

    def list(self, request):
        floors = Floor.objects.all()
        serializer = FloorSerializer(floors, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FloorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            floor = Floor.objects.get(pk=pk)
        except Floor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FloorSerializer(floor)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            floor = Floor.objects.get(pk=pk)
        except Floor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FloorSerializer(floor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            floor = Floor.objects.get(pk=pk)
            floor.delete()
        except Floor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
