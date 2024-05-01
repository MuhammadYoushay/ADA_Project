import time
import matplotlib.pyplot as plt
import networkx as nx

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

def greedy_graph_coloring(graph):
    vertices = list(graph.keys())
    vertex_colors = {}
    for vertex in vertices:
        available_colors = set(range(len(graph)))
        for neighbor in graph[vertex]:
            if neighbor in vertex_colors:
                if vertex_colors[neighbor] in available_colors:
                    available_colors.remove(vertex_colors[neighbor])
        if available_colors:
            vertex_colors[vertex] = min(available_colors)
        else:
            vertex_colors[vertex] = max(vertex_colors.values()) + 1

    return max(vertex_colors.values()) + 1, vertex_colors

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
file_path = 'le450_15b.col'

# Measure execution time
start_time = time.time()

graph = read_graph_from_file(file_path)
chromatic_number, vertex_colors = greedy_graph_coloring(graph)
print(f"The chromatic number of the graph is: {chromatic_number}")
end_time = time.time()
visualize_graph(graph, vertex_colors)
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
