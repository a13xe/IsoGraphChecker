import json
import networkx as nx
from networkx.algorithms import isomorphism


def load_graph_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    G = nx.Graph()
    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'])
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'])
    return G


def vf2_isomorphism(graph1, graph2):
    return isomorphism.GraphMatcher(graph1, graph2)


if __name__ == "__main__":
    graph1 = load_graph_from_json('graphs/graph.json')
    graph2 = load_graph_from_json('graphs/el_graph.json')
    
    is_isomorphic = isomorphism.GraphMatcher(graph1, graph2)
    
    print("Graphs are isomorphic" if is_isomorphic else "Graphs are not isomorphic")
