import networkx as nx
from collections import defaultdict

def weisfeiler_lehman_isomorphism(graph1, graph2, iterations=3):
    def weisfeiler_lehman_step(graph, labels):
        new_labels = {}
        for node in graph.nodes():
            neighborhood = sorted([labels[neighbor] for neighbor in graph.neighbors(node)])
            new_labels[node] = hash(tuple(neighborhood))
        return new_labels

    labels1 = {node: 1 for node in graph1.nodes()}
    labels2 = {node: 1 for node in graph2.nodes()}

    for _ in range(iterations):
        labels1 = weisfeiler_lehman_step(graph1, labels1)
        labels2 = weisfeiler_lehman_step(graph2, labels2)

    label_histogram1 = defaultdict(int)
    label_histogram2 = defaultdict(int)

    for label in labels1.values():
        label_histogram1[label] += 1
    for label in labels2.values():
        label_histogram2[label] += 1

    return label_histogram1 == label_histogram2