# In a separate file, e.g. utils.py

from django.http import JsonResponse
from networkx import shortest_path

from admin_panel.graph_utils import rebuild_graph


def get_path(from_room_id, to_room_id):
    try:
        G = rebuild_graph()
        path = shortest_path(G, source=from_room_id, target=to_room_id)
        return {'path': path}
    except Exception as e:
        return {'error': str(e)}