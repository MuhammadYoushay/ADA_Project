import matplotlib.pyplot as plt
import networkx as nx
from itertools import product
import time

def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('e'):
                _, v1, v2 = line.split()
                v1, v2 = int(v1), int(v2)
                if v1 not in graph:
                    graph[v1] = []
                if v2 not in graph:
                    graph[v2] = []
                graph[v1].append(v2)
                graph[v2].append(v1)
    return graph

def is_valid_coloring(graph, vertex_colors):
    for vertex, neighbors in graph.items():
        vertex_color = vertex_colors[vertex]
        for neighbor in neighbors:
            if vertex_color == vertex_colors[neighbor]:
                return False
    return True

def graph_coloring_brute_force(graph):
    n = len(graph)
    vertices = list(graph.keys())


    
    for num_colors in range(1, n + 1):
        for candidate_colors in product(range(num_colors), repeat=n):
            vertex_colors = dict(zip(vertices, candidate_colors))
            if is_valid_coloring(graph, vertex_colors):
                return num_colors, vertex_colors
    
    return n, {}

def visualize_graph(graph, vertex_colors):
    G = nx.Graph()
    for vertex, neighbors in graph.items():
        G.add_node(vertex)
        for neighbor in neighbors:
            G.add_edge(vertex, neighbor)
    
    color_map = [vertex_colors.get(node, 0) for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=color_map, font_color='white', edge_color='gray', width=0.5 ,cmap=plt.cm.get_cmap('viridis', max(vertex_colors.values())+1))
    plt.show()

# Read graph from file
file_path = 'queen11_11.col'
start_time = time.time()
graph = read_graph_from_file(file_path)
chromatic_number, vertex_colors = graph_coloring_brute_force(graph)
print(f"The chromatic number of the graph is: {chromatic_number}")
end_time = time.time()
visualize_graph(graph, vertex_colors)
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
