import networkx as nx
from django.http import JsonResponse
from networkx import shortest_path
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .graph_utils import rebuild_graph
from .models import Floor, Room
from .serializers import FloorSerializer, RoomSerializer
from rest_framework.decorators import action, api_view
from rest_framework.parsers import JSONParser


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


class RoomViewSet(viewsets.ViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def list(self, request, floor_pk=None):
        floor_pk = request.query_params.get('floor_pk')
        if floor_pk:
            rooms = Room.objects.filter(floor__id=floor_pk)
        else:
            rooms = Room.objects.all()  # Or handle this case as you see fit
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Extract floor_pk from query parameters
        floor_pk = request.query_params.get('floor_pk')
        if not floor_pk:
            return Response({"error": "Floor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the Floor instance using floor_pk
        floor = get_object_or_404(Floor, pk=floor_pk)

        # Deserialize the data
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Room instance with the specified floor
            serializer.save(floor=floor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        floor_pk = request.query_params.get('floor_pk')
        if not floor_pk:
            return Response({"error": "Floor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(Room, pk=pk, floor__id=floor_pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def update(self, request, pk=None):
        floor_pk = request.query_params.get('floor_pk')
        if not floor_pk:
            return Response({"error": "Floor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(Room, pk=pk, floor__id=floor_pk)
        serializer = RoomSerializer(instance=room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        floor_pk = request.query_params.get('floor_pk')
        if not floor_pk:
            return Response({"error": "Floor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        room = get_object_or_404(Room, pk=pk, floor__id=floor_pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # for the path
    # In views.py


def euclidean_heuristic(a, b):
    a_x, a_y = rooms_dict[a]['x'], rooms_dict[a]['y']
    b_x, b_y = rooms_dict[b]['x'], rooms_dict[b]['y']
    return ((a_x - b_x) ** 2 + (a_y - b_y) ** 2) ** 0.5

def find_elevator_on_floor(floor_id):
    elevator = Room.objects.filter(floor_id=floor_id, is_elevator=True).first()
    return elevator.id if elevator else None


def get_path(request, from_room_id, to_room_id):
    G = rebuild_graph()

    # Logic to get the elevator node on the floors
    from_room_floor_id = Room.objects.get(id=from_room_id).floor_id
    to_room_floor_id = Room.objects.get(id=to_room_id).floor_id
    elevator_on_start_floor = find_elevator_on_floor(from_room_floor_id)
    elevator_on_end_floor = find_elevator_on_floor(to_room_floor_id)

    if elevator_on_start_floor is None or elevator_on_end_floor is None:
        return JsonResponse({'error': 'Elevator not found on one of the floors'}, status=404)

    # Get all rooms
    rooms = Room.objects.all().values('id', 'x', 'y', 'floor_id')
    global rooms_dict
    rooms_dict = {room['id']: room for room in rooms}

    # Check if nodes exist in the graph
    if not all(node in G for node in [from_room_id, to_room_id, elevator_on_start_floor, elevator_on_end_floor]):
        return JsonResponse({'error': 'One or more nodes not found in the graph'}, status=400)

    # Find paths using A* algorithm
    path_to_elevator = nx.astar_path(G, source=from_room_id, target=elevator_on_start_floor, heuristic=euclidean_heuristic)
    path_from_elevator = nx.astar_path(G, source=elevator_on_end_floor, target=to_room_id, heuristic=euclidean_heuristic)

    # Combine paths
    complete_path = path_to_elevator + path_from_elevator

    # Prepare the path data
    path_with_coords = [rooms_dict[room_id] for room_id in complete_path if room_id in rooms_dict]

    return JsonResponse(path_with_coords, safe=False)