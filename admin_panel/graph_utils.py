from .models import Room, Connection
import networkx as nx
import numpy as np


def calculate_distance(room1, room2):
    return np.sqrt((room1['x'] - room2['x']) ** 2 + (room1['y'] - room2['y']) ** 2)


def rebuild_graph():
    floors = Room.objects.values_list('floor', flat=True).distinct()
    master_graph = nx.Graph()

    elevators = {}

    for floor_id in floors:
        floor_rooms = list(Room.objects.filter(floor=floor_id).values('id', 'x', 'y', 'is_elevator'))
        floor_graph = make_algo(floor_rooms)

        master_graph.add_nodes_from(floor_graph.nodes(data=True))
        master_graph.add_edges_from(floor_graph.edges(data=True))

        elevator_node = next((node for node, data in floor_graph.nodes(data=True) if data['is_elevator']), None)
        if elevator_node:
            elevators[floor_id] = elevator_node

    for floor_id, elevator_node in elevators.items():
        # Check if there's an elevator on the next floor
        next_floor_elevator_node = elevators.get(floor_id + 1)
        if next_floor_elevator_node:
            # Connect the current floor elevator with the next floor elevator
            master_graph.add_edge(elevator_node, next_floor_elevator_node)

    return master_graph



def make_algo(rooms_data):
    G = nx.Graph()

    # Identify the elevator and add it as a node
    elevator_room = next((room for room in rooms_data if room['is_elevator']), None)
    if not elevator_room:
        raise ValueError("No elevator room found")

    G.add_node(elevator_room['id'], pos=(elevator_room['x'], elevator_room['y']),is_elevator=True)

    # Connect rooms within 10 units in x to the elevator
    vertical_line_rooms = [elevator_room]
    for room in rooms_data:
        if room['id'] != elevator_room['id'] and abs(room['x'] - elevator_room['x']) <= 20:
            G.add_node(room['id'], pos=(room['x'], room['y']),is_elevator=False)
            vertical_line_rooms.append(room)

    # Sort rooms in the vertical line by y-coordinate
    vertical_line_rooms.sort(key=lambda room: room['y'])

    # Connect each room to its subsequent room in the sorted list
    for i in range(len(vertical_line_rooms) - 1):
        room1 = vertical_line_rooms[i]
        room2 = vertical_line_rooms[i + 1]
        G.add_edge(room1['id'], room2['id'])

    # For each remaining room, find the nearest room in the vertical line based on y-distance
    for room in rooms_data:
        if room not in vertical_line_rooms:
            G.add_node(room['id'], pos=(room['x'], room['y']),is_elevator=False)
            nearest_in_y = min(vertical_line_rooms, key=lambda r: abs(r['y'] - room['y']))
            G.add_edge(room['id'], nearest_in_y['id'])

    for room_id, connected_room_id in G.edges():
        room1 = next(r for r in rooms_data if r['id'] == room_id)
        room2 = next(r for r in rooms_data if r['id'] == connected_room_id)
        distance = calculate_distance(room1, room2)
        Connection.objects.update_or_create(
            from_room_id=room_id, to_room_id=connected_room_id,
            defaults={'distance': distance}
        )

    return G
