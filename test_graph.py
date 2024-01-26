import os
import django
import networkx as nx
import matplotlib.pyplot as plt

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'floor_nav.settings')
django.setup()

# Now you can import your Django models
from admin_panel.models import Room  # Adjust the import path if necessary

# Assuming rebuild_graph returns a NetworkX graph object
from admin_panel.graph_utils import rebuild_graph


# Function to build and return the graph
def plot_graph(G):
    # Make sure G is indeed a graph object


    # Use spring_layout to space out nodes
    pos = nx.spring_layout(G)

    # Increase spacing between nodes
    k = 0.5
    pos_adjusted = {node: (x * k, y * k) for node, (x, y) in pos.items()}

    # Draw graph with curved edges
    nx.draw(G, pos_adjusted, with_labels=True, edge_color='black', width=1, edge_cmap=plt.get_cmap('jet'),
            connectionstyle='arc3, rad=0.1')

    plt.axis('off')
    plt.show()


# This function builds the master graph and calls plot_graph to visualize it
def build_and_plot_graph():
    master_graph = rebuild_graph()  # rebuild_graph should return a single NetworkX graph object

    # Check if master_graph is a NetworkX graph object
    if isinstance(master_graph, nx.Graph):
        plot_graph(master_graph)
    else:
        print("master_graph is not a NetworkX graph object")


# Main execution
if __name__ == '__main__':
    build_and_plot_graph()
