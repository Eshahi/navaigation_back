import networkx as nx
from admin_panel.models import Room  # Import your Room model


def build_graph():
    rooms = Room.objects.all()
    G = nx.Graph()
    # Add your algorithm to add nodes and edges based on the rooms
    # ...
    return G


def find_path(graph, start_id, end_id):
    path = nx.shortest_path(graph, source=start_id, target=end_id)
    return path
