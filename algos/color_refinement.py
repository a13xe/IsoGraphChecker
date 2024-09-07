import json
import networkx as nx
from collections import defaultdict


def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'])
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    return G


def get_node_labels(graph):
    labels = nx.get_node_attributes(graph, 'label')
    return {node: labels[node] for node in graph.nodes()}


def color_refinement_hash(graph, iterations):
    labels = get_node_labels(graph)
    for _ in range(iterations):
        new_labels = {}
        for node in graph.nodes():
            neighbor_labels = sorted(labels[neighbor] for neighbor in graph.neighbors(node))
            new_labels[node] = labels[node] + ''.join(str(label) for label in neighbor_labels)
        label_map = defaultdict(int)
        for label in new_labels.values():
            label_map[label] += 1
        new_label_map = {label: str(i) for i, label in enumerate(sorted(label_map.keys()))}
        labels = {node: new_label_map[label] for node, label in new_labels.items()}
    return set(labels.values())


def color_refinement_isomorphism(graph1, graph2, iterations=3):
    hash1 = color_refinement_hash(graph1, iterations)
    hash2 = color_refinement_hash(graph2, iterations)
    return hash1 == hash2


if __name__ == "__main__":
    graph1 = load_graph_from_json('graphs/graph.json')
    graph2 = load_graph_from_json('graphs/el_graph.json')
    
    is_isomorphic = color_refinement_isomorphism(graph1, graph2)
    print("Graphs are isomorphic" if is_isomorphic else "Graphs are not isomorphic")
